// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AuditLog {
    // Mapping employee ID (string) to hash
    mapping(string => string) private employeeHashes;

    // Event emitted whenever a hash is added or updated
    event HashAdded(string indexed employeeId, string recordHash, uint256 timestamp);
    event HashUpdated(string indexed employeeId, string oldHash, string newHash, uint256 timestamp);

    // Contract owner (optional control)
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }

    // Add or update hash
    function addHash(string memory employeeId, string memory recordHash) public {
        require(bytes(employeeId).length > 0, "Employee ID cannot be empty");
        require(bytes(recordHash).length > 0, "Hash cannot be empty");

        if (bytes(employeeHashes[employeeId]).length == 0) {
            // First time addition
            employeeHashes[employeeId] = recordHash;
            emit HashAdded(employeeId, recordHash, block.timestamp);
        } else {
            // Updating existing hash
            string memory oldHash = employeeHashes[employeeId];
            employeeHashes[employeeId] = recordHash;
            emit HashUpdated(employeeId, oldHash, recordHash, block.timestamp);
        }
    }

    // Fetch hash with existence check
    function getHash(string memory employeeId) public view returns (string memory) {
        string memory recordHash = employeeHashes[employeeId];
        require(bytes(recordHash).length > 0, "Employee hash not found on chain");
        return recordHash;
    }

    // Optional: Owner can remove a hash (for auditing or correction)
    function removeHash(string memory employeeId) public onlyOwner {
        require(bytes(employeeHashes[employeeId]).length > 0, "Employee hash does not exist");
        delete employeeHashes[employeeId];
    }

    // Security/Integrity audit: Check if an ID exists
    function exists(string memory employeeId) public view returns (bool) {
        return bytes(employeeHashes[employeeId]).length > 0;
    }
}
