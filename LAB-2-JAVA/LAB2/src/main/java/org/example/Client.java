package org.example;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import java.io.*;
import java.net.Socket;
import java.security.PublicKey;
import java.util.Base64;
import java.io.File;

public class Client {
    private static final String HOST = "127.0.0.1";
    private static final int PORT = 3161;
    private static SecretKey secretKey;

    public static void main(String[] args) {
        try {
            secretKey = generateSecretKey();

            Socket socket = new Socket(HOST, PORT);
            System.out.println("Connected to server");

            ObjectInputStream in = new ObjectInputStream(socket.getInputStream());
            PublicKey serverPublicKey = (PublicKey) in.readObject();

            String encryptedSecretKey = encryptSecretKey(serverPublicKey);
            System.out.println("Secret key encrypted successfully");

            ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
            out.writeObject(encryptedSecretKey);

            String data = "hello";
            String encryptedData = encryptData(data);
            System.out.println("Data encrypted successfully");

            out.writeObject(encryptedData);

            String readData = (String) in.readObject();

            if (!readData.isEmpty()) {
                File file = new File("client_ledger.json");

                if (file.createNewFile()) {
                    try {
                        FileWriter write = new FileWriter(file);
                        BufferedWriter writer = new BufferedWriter(write);

                        writer.write(readData);
                        writer.newLine();

                        writer.close();
                    } catch (IOException E) {
                        E.printStackTrace();
                    }
                }
            }

            socket.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static SecretKey generateSecretKey() throws Exception {
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(128);
        return keyGen.generateKey();
    }

    private static String encryptSecretKey(PublicKey publicKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);
        byte[] encryptedBytes = cipher.doFinal(secretKey.getEncoded());
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }

    private static String encryptData(String data) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        byte[] encryptedBytes = cipher.doFinal(data.getBytes());
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }
}