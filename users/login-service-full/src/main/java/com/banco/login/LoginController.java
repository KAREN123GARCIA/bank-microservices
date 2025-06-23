package com.banco.login;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Optional;

@RestController
@RequestMapping("/login")
public class LoginController {
    @Autowired
    private CustomerRepository repository;

    @PostMapping
    public ResponseEntity<?> login(@RequestBody Customer request) {
        Optional<Customer> user = repository.findByMailAndHashPassword(request.getMail(), request.getHashPassword());
        return user.isPresent() ?
            ResponseEntity.ok("Login exitoso") :
            ResponseEntity.status(401).body("Credenciales inválidas");
    }
}