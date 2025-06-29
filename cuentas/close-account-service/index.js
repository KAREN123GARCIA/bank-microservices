const express = require('express');
const soap = require('strong-soap').soap;
const fs = require('fs');
const http = require('http');
const pg = require('pg');

const pool = new pg.Pool({
  user: 'karen',
  host: 'postgres-login',
  database: 'cuentas_db',
  password: '2007',
  port: 5432,
});

const service = {
  AccountService: {
    AccountServicePort: {
      CloseAccount(args, callback) {
        const { accountId } = args;

        pool.query(
          'UPDATE accounts SET state = $1 WHERE id_account = $2 RETURNING id_account',
          ['CLOSED', accountId],
          (err, result) => {
            if (err || result.rows.length === 0) {
              console.error('Error al cerrar cuenta:', err);
              callback({ error: 'No se pudo cerrar la cuenta o no existe' });
            } else {
              console.log('Cuenta cerrada:', result.rows[0]);
              callback({ accountId: result.rows[0].id_account });
            }
          }
        );
      }
    }
  }
};

const xml = fs.readFileSync('close-account.wsdl', 'utf8');
const app = express();
const server = http.createServer(app);
soap.listen(server, '/wsdl', service, xml);
server.listen(8087, () => {
  console.log('SOAP CloseAccountService corriendo en puerto 8087');
});
