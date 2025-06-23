package com.banco.verifyemailservice;
import jakarta.persistence.*;

@Entity
@Table(name = "customers")
public class entity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id_users;
    private String mail;

    public String getMail() { return mail; }
    public void setMail(String mail) { this.mail = mail; }
}