const bcrypt = require("bcryptjs")

const knobbe_apikey = "0f500c90-9df1-4bd4-b789-b89f1a1bcf65"
const isotimestamp = new Date().toISOString();
const authhash = knobbe_apikey + "|" + isotimestamp;

const cryptfunction = async () => {
    const hashedKey = await bcrypt.hash(authhash, 10)
    console.log(knobbe_apikey);
    console.log(isotimestamp);
    console.log(hashedKey);
};


cryptfunction()

