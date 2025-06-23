package com.banco.verifyemailservice;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Optional;

@RestController
@RequestMapping("/verify-email")
public class controller {
    @Autowired
    private repository repo;

    @GetMapping("/{email}")
    public ResponseEntity<?> verify(@PathVariable String email) {
        String normalizedMail = email.trim().toLowerCase();
        Optional<entity> user = repo.findByMail(normalizedMail);
        return user.isPresent() ?
            ResponseEntity.ok("Correo verificado") :
            ResponseEntity.status(404).body("Correo no encontrado");
    }
}