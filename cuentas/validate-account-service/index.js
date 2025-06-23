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
      ValidateAccount(args, callback) {
        const { accountId } = args;

        pool.query(
          'SELECT state FROM accounts WHERE id_account = $1',
          [accountId],
          (err, result) => {
            if (err || result.rows.length === 0) {
              console.error('Error al validar cuenta:', err);
              callback({ isActive: false });
            } else {
              const isActive = result.rows[0].state === 'ACTIVE';
              callback({ isActive });
            }
          }
        );
      }
    }
  }
};

const xml = fs.readFileSync('validate-account.wsdl', 'utf8');
const app = express();
const server = http.createServer(app);
soap.listen(server, '/wsdl', service, xml);
server.listen(8088, () => {
  console.log('SOAP ValidateAccountService corriendo en puerto 8088');
});
