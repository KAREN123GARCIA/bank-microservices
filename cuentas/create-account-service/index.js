const express = require('express');
const soap = require('strong-soap').soap;
const fs = require('fs');
const http = require('http');
const pg = require('pg');
const path = require('path');

// PostgreSQL connection
const pool = new pg.Pool({
  user: 'karen',
  host: 'postgres-login',
  database: 'cuentas_db',
  password: '2007',
  port: 5432,
});

// SOAP service definition
const service = {
  AccountService: {
    AccountServiceSoapPort: {
      CreateAccount(args, callback) {
        const { userId, currency, balance } = args;

        pool.query(
          'INSERT INTO accounts (user_id, currency, balance, state, creation_date) VALUES ($1, $2, $3, $4, NOW()) RETURNING id_account',
          [userId, currency, balance, 'ACTIVE'],
          (err, result) => {
            if (err) {
              console.error('Error al crear cuenta:', err);
              callback({ error: err.message });
            } else {
              console.log('Cuenta creada con ID:', result.rows[0].id_account);
              callback(null, { accountId: result.rows[0].id_account });
            }
          }
        );
      }
    }
  }
};

// Leer archivo WSDL
const wsdlPath = path.join(__dirname, 'account.wsdl');
const xml = fs.readFileSync(wsdlPath, 'utf8');

// Crear y levantar servidor
const app = express();
const server = http.createServer(app);

soap.listen(server, '/wsdl', service, xml);

server.listen(8085, () => {
  console.log('✅ SOAP AccountService activo en puerto 8085');
});
