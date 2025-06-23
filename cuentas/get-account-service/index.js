const express = require('express');
const soap = require('strong-soap').soap;
const fs = require('fs');
const http = require('http');
const pg = require('pg');

// Conexión a PostgreSQL
const pool = new pg.Pool({
  user: 'karen',
  host: 'postgres-login',
  database: 'cuentas_db',
  password: '2007',
  port: 5432,
});

const app = express();
app.use(express.json()); // Para poder leer JSON en requests

// Servicio SOAP
const service = {
  AccountService: {
    AccountServicePort: {
      GetAccount(args, callback) {
        const { accountId } = args;
        pool.query(
          'SELECT user_id, balance, currency, state FROM accounts WHERE id_account = $1',
          [accountId],
          (err, result) => {
            if (err || result.rows.length === 0) {
              console.error('Error o cuenta no encontrada:', err);
              callback({ error: 'Cuenta no encontrada o error en la consulta' });
            } else {
              const row = result.rows[0];
              console.log('✅ Cuenta encontrada:', row);
              callback({
                userId: row.user_id,
                balance: row.balance,
                currency: row.currency,
                state: row.state,
              });
            }
          }
        );
      }
    }
  }
};

// Lectura del archivo WSDL
const xml = fs.readFileSync('get-account.wsdl', 'utf8');

// Crear servidor SOAP
const server = http.createServer(app);
soap.listen(server, '/wsdl', service, xml);

// Endpoint REST: obtener cuenta por ID
app.get('/account/:id', (req, res) => {
  const accountId = parseInt(req.params.id);
  pool.query(
    'SELECT user_id, balance, currency, state FROM accounts WHERE id_account = $1',
    [accountId],
    (err, result) => {
      if (err || result.rows.length === 0) {
        return res.status(404).json({ error: 'Cuenta no encontrada' });
      }
      res.json(result.rows[0]);
    }
  );
});

// Endpoint REST: actualizar saldo
app.put('/account/:id', (req, res) => {
  const accountId = parseInt(req.params.id);
  const { balance } = req.body;

  if (isNaN(balance)) {
    return res.status(400).json({ error: 'El saldo debe ser un número válido' });
  }

  pool.query(
    'UPDATE accounts SET balance = $1 WHERE id_account = $2',
    [balance, accountId],
    (err, result) => {
      if (err) {
        console.error('❌ Error al actualizar saldo:', err);
        return res.status(500).json({ error: 'Error al actualizar saldo' });
      }
      if (result.rowCount === 0) {
        return res.status(404).json({ error: 'Cuenta no encontrada para actualizar' });
      }
      res.status(200).json({ message: 'Saldo actualizado exitosamente' });
    }
  );
});

// Iniciar servidor
server.listen(8086, () => {
  console.log('🟢 SOAP GetAccountService corriendo en http://localhost:8086/wsdl');
});

