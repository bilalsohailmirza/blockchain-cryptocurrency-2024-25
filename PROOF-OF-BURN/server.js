const express = require("express");
const cors = require("cors");
const app = express();
const fs = require("fs");
const crypto = require("crypto");
const path = require("path");

app.use(cors());
const FILE_PATH = path.join(__dirname, "blockchain_logs.json");

let logs = require(FILE_PATH);

app.listen(3161, () => {
    console.log("[server.logs] Server is listening at port 3161");
    // console.log(logs.leaf_nodes["02c6edc2ad3e1f2f9a9c8fea18c0702c4d2d753440315037bc7f84ea4bba2542"]);
    // console.log(logs.root_hash);
});

// FIX THE COMPARASION OF HASHES OF USERADDRESS AND USERADDRESS+SIGNATURE
app.post('/burn/:useraddr/:signature/:burnamount/', (req, res) => {
    const { useraddr, burnamount, signature } = req.params;

    if (useraddr, signature) {
        if (logs.leaf_nodes.hasOwnProperty(useraddr)) {
            const CURR_COIN_VAL = parseInt(logs.leaf_nodes[useraddr].CURR_COIN_VAL);

            if (CURR_COIN_VAL >= parseInt(burnamount) && logs.leaf_nodes[useraddr].TRANSFER_READY === true) {
            
            const TX_HASH = crypto.createHash("sha256").update(signature+'0000000000000000000000000000000000000000000000000000000000000000'+burnamount.toString()+logs.root_hash).digest('hex');
            console.log(TX_HASH);
            console.log(logs.leaf_nodes[useraddr].TRANSFER_HISTORY.OUTGOING);
            console.log(logs.leaf_nodes['0000000000000000000000000000000000000000000000000000000000000000'].TRANSFER_HISTORY.INCOMING);


            logs.leaf_nodes[useraddr].CURR_COIN_VAL = CURR_COIN_VAL - parseInt(burnamount);
            logs.leaf_nodes[useraddr].TRANSFER_HISTORY.OUTGOING[TX_HASH] = parseInt(burnamount);
            logs.root_hash = crypto.createHash("sha256").update(logs.root_hash).digest('hex');

            logs.leaf_nodes['0000000000000000000000000000000000000000000000000000000000000000'].CURR_COIN_VAL += parseInt(burnamount);
            logs.leaf_nodes['0000000000000000000000000000000000000000000000000000000000000000'].TRANSFER_HISTORY.INCOMING[TX_HASH] = parseInt(burnamount);

            fs.writeFile(FILE_PATH, JSON.stringify(logs, null, 2), (err) => {
                if (err) {
                    console.error('Error saving data to JSON file:', err);
                    return res.status(500).send('Error saving data');
                }
                console.log('Data successfully saved to JSON file');
                verify(useraddr, TX_HASH);
                return res.send(`Address ${useraddr} updated with new coin value: ${logs.leaf_nodes[useraddr].CURR_COIN_VAL}`);
            });
            }
            else {
                return res.send(`Address ${useraddr} does not have enough coin value to burn`); 
            }
        }
    }
});

app.post('/register/:name/:signature/', (req, res) => {
    const { name, signature } = req.params;

    const NAME = crypto.createHash("sha256").update(name).digest('hex');
    const SIGNATURE = crypto.createHash("sha256").update(signature).digest('hex');

    const useraddr = crypto.createHash("sha256").update(crypto.createHash("sha256").update(NAME+SIGNATURE).digest('hex')).digest('hex');

    if (name && signature) {
        if (logs.leaf_nodes.hasOwnProperty(useraddr)) {
            return res.send(`You are already a member of the chain.`);
        } else {
            logs.leaf_nodes[useraddr] = {
                CURR_COIN_VAL: 0,
                NAME: name,
                TRANSFER_READY: true,
                TRANSFER_HISTORY: {
                    "0000000000000000000000000000000000000000000000000000000000000000": 0
                }
            }
            logs.root_hash = crypto.createHash("sha256").update(useraddr).digest('hex');

            fs.writeFile(FILE_PATH, JSON.stringify(logs, null, 2), (err) => {
                if (err) {
                    console.error('Error saving data to JSON file:', err);
                    return res.status(500).send('Error saving data');
                }
                console.log('User succesfully joined the chain');
                return res.send(`Address ${useraddr} joined the chain with details: ${logs.leaf_nodes[useraddr]}`);
            });
        }
    }
});

// REMAINING: LOGIN
app.post('/login/:useraddr/:signature/', (req, res) => {
    const { useraddr, signature } = req.params;

    if (useraddr && signature) {
        
    }
});

function verify(useraddr, TX_HASH) {
    if (logs.leaf_nodes['0000000000000000000000000000000000000000000000000000000000000000'].TRANSFER_HISTORY.INCOMING[TX_HASH] === logs.leaf_nodes[useraddr].TRANSFER_HISTORY.OUTGOING[TX_HASH]) {
        console.log("verified, proceed to login");
        return;
    } else {
        console.log("not verified, please try again");
    }
}