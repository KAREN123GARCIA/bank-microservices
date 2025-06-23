package com.banco.resetpasswordservice;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/reset-password")
public class controller {

    @Autowired
    private repository repo;

    @PutMapping("/{email}")
    public ResponseEntity<?> reset(@PathVariable String email, @RequestBody entity body) {
        String normalizedMail = email.trim().toLowerCase();  // ✅ normalizar email

        Optional<entity> found = repo.findByMail(normalizedMail);
        if (found.isPresent()) {
            entity user = found.get();
            user.setHashPassword(body.getHashPassword());
            repo.save(user);
            return ResponseEntity.ok("Contraseña actualizada");
        } else {
            return ResponseEntity.status(404).body("Usuario no encontrado");
        }
    }
}
