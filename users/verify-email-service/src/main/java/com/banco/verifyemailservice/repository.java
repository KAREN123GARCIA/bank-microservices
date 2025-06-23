package com.banco.verifyemailservice;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface repository extends JpaRepository<entity, Integer> {
    Optional<entity> findByMail(String mail);
}