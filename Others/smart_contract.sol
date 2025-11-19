// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AuditLog {
    // Mapping from employee name to their record hash
    mapping(string => bytes32) private recordHashes;
    
    // Event emitted when a hash is added
    event HashAdded(string indexed name, bytes32 recordHash, uint256 timestamp);
    
    // Add or update a hash for an employee record
    function addHash(string memory name, bytes32 recordHash) public {
        require(bytes(name).length > 0, "Name cannot be empty");
        require(recordHash != bytes32(0), "Hash cannot be empty");
        
        recordHashes[name] = recordHash;
        emit HashAdded(name, recordHash, block.timestamp);
    }
    
    // Retrieve the hash for a given employee
    function getHash(string memory name) public view returns (bytes32) {
        return recordHashes[name];
    }
    
    // Check if a hash exists for an employee
    function hashExists(string memory name) public view returns (bool) {
        return recordHashes[name] != bytes32(0);
    }
}
