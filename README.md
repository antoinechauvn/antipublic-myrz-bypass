# antipublic-myrz-bypass
Exploit for Antipublic.one

### Qu'est-ce que MYRZ?
>AntiPublic MYRZ de vérification de base privée dans le but de vérifier la sécurité de ses données.<br>
Il est accessible au prix de 3,5 $

## Fonctionnement
Antipublic Myrz utilise le principe de `GUID` introduit par microsoft afin de garantir que l'authenticité du destinataire.

L'`UUID` et le `GUID` sont des identifiants de 128 bits. L'UUID est défini par l'IETF RFC4122 alors que le GUID a été défini par Microsoft pour le système d'exploitation Windows. Si vous creusez dans les définitions, vous pouvez trouver quelques nuances sur les données utilisées pour générer des octets spécifiques d'un UUID/GUID, mais à toutes fins utiles, ils sont identiques et peuvent être utilisés sur tous les systèmes.

On peux retrouver la GUID de la machine à l'emplacement `SOFTWARE\\Microsoft\\Cryptography`
```csharp
private static string GetID() {
  string text = "SOFTWARE\\Microsoft\\Cryptography";
  string text2 = "MachineGuid";
  string result;
  using(RegistryKey registryKey = RegistryKey.OpenBaseKey(RegistryHive.LocalMachine, RegistryView.Registry64)) {
    using(RegistryKey registryKey2 = registryKey.OpenSubKey(text)) {
      if (registryKey2 == null) {
        throw new KeyNotFoundException(string.Format("Key Not Found: {0}", text));
      }
      object value = registryKey2.GetValue(text2);
      if (value == null) {
        throw new IndexOutOfRangeException(string.Format("Index Not Found: {0}", text2));
      }
      result = value.ToString();
    }
  }
  return result;
}
}
}
```
Par la suite Antipublic Myrz génére une clé de configuration (config.key) basée sur le GUID, un encodage en UTF-16 Little-Endian ainsi qu'un chiffrement en MD5.<br>
Le chiffrement Message Digest 5 est deprécié depuis 2004 du à une découverte de collisions (https://fr.wikipedia.org/wiki/MD5).
```csharp
private static string GetHashString(string s) {
  byte[] array = new MD5CryptoServiceProvider().ComputeHash(Encoding.Unicode.GetBytes(s));
  string text = string.Empty;
  foreach(byte b in array) {
    text += string.Format("{0:x2}", b);
  }
  return text;
}
```

On consulte ensuite via l'api si la key est valide.
```python
def key_check(key):
    req = requests.get(f'http://antipublic.one/api/check.php?key={key}')
    data = req.json()
    print(data)
```

<hr>
### Générer une clé et l'activer
On va créer une clé random basée sur 16 octets
```python
def key_generate():
    random_key = secrets.token_hex(16)  # https://docs.python.org/3/library/secrets.html#secrets.token_hex
    print(f"{colorama.Fore.LIGHTYELLOW_EX}[~]Activating {random_key}")
    key_activation(random_key)
```
