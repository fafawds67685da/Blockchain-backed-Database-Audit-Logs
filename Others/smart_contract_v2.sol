// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AuditLogV2 {
    // Mapping from employee ID to their record hash
    mapping(uint256 => bytes32) private recordHashes;
    
    // Event emitted when a hash is added
    event HashAdded(uint256 indexed employeeId, bytes32 recordHash, uint256 timestamp);
    
    // Add or update a hash for an employee record
    function addHash(uint256 employeeId, bytes32 recordHash) public {
        require(employeeId > 0, "Employee ID must be greater than 0");
        require(recordHash != bytes32(0), "Hash cannot be empty");
        
        recordHashes[employeeId] = recordHash;
        emit HashAdded(employeeId, recordHash, block.timestamp);
    }
    
    // Retrieve the hash for a given employee ID
    function getHash(uint256 employeeId) public view returns (bytes32) {
        return recordHashes[employeeId];
    }
    
    // Check if a hash exists for an employee
    function hashExists(uint256 employeeId) public view returns (bool) {
        return recordHashes[employeeId] != bytes32(0);
    }
}
