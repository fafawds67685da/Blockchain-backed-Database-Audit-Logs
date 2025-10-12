// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AuditLog {
    mapping(string => string) private employeeHashes;

    function addHash(string memory name, string memory recordHash) public {
        // Ensure name is not empty if it's used as a key
        require(bytes(name).length > 0, "Name cannot be empty");
        employeeHashes[name] = recordHash;
    }

    function getHash(string memory name) public view returns (string memory) {
        string memory recordHash = employeeHashes[name];
        
        // 🚨 CRITICAL FIX: Explicitly check if the hash exists. 
        // If the hash is an empty string (""), the key was not found.
        // Reverting here provides a clearer error than an "invalid opcode."
        require(bytes(recordHash).length > 0, "Employee hash not found on chain");
        
        return recordHash;
    }
}