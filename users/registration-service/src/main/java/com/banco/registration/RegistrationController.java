package com.banco.registration;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/register")
public class RegistrationController {
    @Autowired
    private CustomerRepository repository;

    @PostMapping
    public ResponseEntity<?> register(@RequestBody Customer customer) {
        if (repository.findByMail(customer.getMail()).isPresent()) {
            return ResponseEntity.badRequest().body("Usuario ya registrado");
        }
        repository.save(customer);
        return ResponseEntity.ok("Usuario registrado exitosamente");
    }
}