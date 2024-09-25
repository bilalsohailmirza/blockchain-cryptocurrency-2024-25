package org.example;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.security.*;
import java.util.Base64;

public class Server {

    private static final int PORT = 3161;
    private static PrivateKey privateKey;
    private static SecretKey secretKey;

    public static void main(String[] args) {
        try {
            KeyPairGenerator keyPairGen = KeyPairGenerator.getInstance("RSA");
            keyPairGen.initialize(2048);
            KeyPair keyPair = keyPairGen.generateKeyPair();
            privateKey = keyPair.getPrivate();
            PublicKey publicKey = keyPair.getPublic();

            ServerSocket serverSocket = new ServerSocket(PORT);
            System.out.println("Server is listening on port " + PORT);

            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Connected to client");

                ObjectOutputStream out = new ObjectOutputStream(clientSocket.getOutputStream());
                out.writeObject(publicKey);
                out.flush();

                ObjectInputStream in = new ObjectInputStream(clientSocket.getInputStream());
                String encryptedSecretKey = (String) in.readObject();
                secretKey = decryptSecretKey(encryptedSecretKey);
                System.out.println("Secret key decrypted successfully");

                String encryptedData = (String) in.readObject();
                String decryptedData = decryptData(encryptedData);
                System.out.println("Decrypted data from client: " + decryptedData);

                String updatedLedger = updateLedger(decryptedData);
                out.writeObject(updatedLedger);
                out.flush();

                clientSocket.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static SecretKey decryptSecretKey(String encryptedSecretKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.DECRYPT_MODE, privateKey);
        byte[] decodedBytes = Base64.getDecoder().decode(encryptedSecretKey);
        byte[] decryptedBytes = cipher.doFinal(decodedBytes);
        return new SecretKeySpec(decryptedBytes, "AES");
    }

    private static String decryptData(String encryptedData) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        byte[] decodedBytes = Base64.getDecoder().decode(encryptedData);
        byte[] decryptedBytes = cipher.doFinal(decodedBytes);
        return new String(decryptedBytes);
    }

    private static String updateLedger(String data) throws IOException, NoSuchAlgorithmException {

        MessageDigest digest = MessageDigest.getInstance("SHA-256");

        // Compute the hash
        byte[] hashBytes = digest.digest(data.getBytes());

        String key = Base64.getEncoder().encodeToString(hashBytes);
        String reverseKey = new StringBuilder(key).reverse().toString();

        StringBuilder ledgerBuilder = new StringBuilder();
        ledgerBuilder.append("[\n");
        ledgerBuilder.append("  {\n");
        ledgerBuilder.append("    \"key\": \"").append(key).append("\",\n");
        ledgerBuilder.append("    \"reverse_key\": \"").append(reverseKey).append("\",\n");
        ledgerBuilder.append("    \"data\": \"").append(data).append("\"\n");
        ledgerBuilder.append("  }\n");
        ledgerBuilder.append("]\n");

        try (FileWriter file = new FileWriter("server_ledger.json")) {
            file.write(ledgerBuilder.toString());
        }

        return ledgerBuilder.toString();
    }
}
