db = db.getSiblingDB('upa')

db.createUser({
    user: 'user',
    pwd: 'passwd',
    roles: [
      {
        role: 'readWrite',
        db: 'upa',
      },
    ],
  });

// TODO: insert data