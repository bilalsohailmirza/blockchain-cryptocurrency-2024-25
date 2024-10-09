# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 10:02:43 2024

@author: Anabia
"""

import hashlib
import json

# Hashing function using SHA-256
def hash_function(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# Function to create a Merkle Tree from a list of data
def create_merkle_tree(data_list):
    if len(data_list) == 1:
        return data_list  # If only one node, it's the root

    new_level = []
    # Pairwise hash nodes together
    for i in range(0, len(data_list), 2):
        left = data_list[i]
        right = data_list[i + 1] if (i + 1) < len(data_list) else data_list[i]  # Handle odd number of elements
        new_hash = hash_function(left + right)
        new_level.append(new_hash)
    return create_merkle_tree(new_level)

# Function to generate Merkle Tree from initial data
def build_merkle_tree(data):
    # Hash individual leaves
    leaf_nodes = [hash_function(item) for item in data]
    # Construct the full tree by recursive hashing
    merkle_tree = create_merkle_tree(leaf_nodes)
    return leaf_nodes, merkle_tree

# Store hash addresses in a JSON file
def store_hashes(leaf_nodes, root_hash):
    tree_data = {
        "leaf_nodes": leaf_nodes,
        "root_hash": root_hash
    }
    with open("merkle_tree.json", "w") as f:
        json.dump(tree_data, f, indent=4)
    print("Merkle Tree hash addresses saved to merkle_tree.json")

# Search for a hash in the JSON file
def search_hash(hash_value):
    with open("merkle_tree.json", "r") as f:
        tree_data = json.load(f)
    
    if hash_value in tree_data["leaf_nodes"] or hash_value == tree_data["root_hash"]:
        print(f"Hash {hash_value} found in the tree!")
    else:
        print(f"Hash {hash_value} not found in the tree.")

# Main execution block
if __name__ == "__main__":
    # Sample data (can be any list of strings)
    data = ["data1", "data2", "data3", "data4"]

    # Build the Merkle Tree
    leaf_nodes, root_hash = build_merkle_tree(data)
    
    # Store hashes in JSON format
    store_hashes(leaf_nodes, root_hash[0])

    # Prompt user for a hash to search
    hash_to_search = input("Enter a hash to search: ")
    search_hash(hash_to_search)