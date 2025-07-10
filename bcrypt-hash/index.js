import bcrypt from 'bcryptjs';

const authhash = {knobbe_apikey}|{isotimestamp};
console.log({
    authhash,
    hashed: bcrypt.hashSync(authhash, 10),
    timestamp: new Date().toISOString()
})