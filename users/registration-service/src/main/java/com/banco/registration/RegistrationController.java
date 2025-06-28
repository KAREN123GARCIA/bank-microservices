package com.banco.registration;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/register")
public class RegistrationController {

    @Autowired
    private CustomerRepository repository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @PostMapping
    public ResponseEntity<?> register(@RequestBody Customer customer) {
        if (repository.findByMail(customer.getMail()).isPresent()) {
            return ResponseEntity.badRequest().body("Usuario ya registrado");
        }

        // Encriptar contraseña antes de guardar
        customer.setHashPassword(passwordEncoder.encode(customer.getHashPassword()));

        repository.save(customer);
        return ResponseEntity.ok("Usuario registrado exitosamente");
    }
}
