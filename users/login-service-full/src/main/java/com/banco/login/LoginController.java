package com.banco.login;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/login")
public class LoginController {

    @Autowired
    private CustomerRepository repository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @PostMapping
    public ResponseEntity<?> login(@RequestBody LoginRequest request) {
        Optional<Customer> userOpt = repository.findByMail(request.getMail());

        if (userOpt.isEmpty()) {
            return ResponseEntity.status(401).body("Usuario no encontrado");
        }

        Customer user = userOpt.get();

        boolean passwordMatch = passwordEncoder.matches(request.getPassword(), user.getHashPassword());

        if (passwordMatch) {
            return ResponseEntity.ok("Login exitoso");
        } else {
            return ResponseEntity.status(401).body("Credenciales inválidas");
        }
    }
}
