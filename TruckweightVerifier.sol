// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract TruckWeightVerifier {
    uint256 public originalWeight;
    uint8 public submissionCount;

    event WeightSubmitted(
        uint8 checkpointNumber,
        uint256 submittedWeight,
        bool isMatching
    );

    constructor(uint256 _originalWeight) {
        originalWeight = _originalWeight;
        submissionCount = 0;
    }

    function submitCheckpointWeight(uint256 newWeight) public {
        require(submissionCount < 3, "All 3 checkpoints already submitted");

        bool matches = (newWeight == originalWeight);
        submissionCount++;

        emit WeightSubmitted(submissionCount, newWeight, matches);
    }
}
