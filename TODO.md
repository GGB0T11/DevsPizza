### ADD:

- Create inflow no Movement
- Adicionar filtros ao list
- Adicionar os forms de volta nos create e update em caso de erro
- Adicionar diferentes unidades de medida aos ingredientes
- Adicionar preco medio aos ingredientes e produtos (talvez)
- Adicionar paginação ao MovementList
- Terminar o MovementCreate, falta o template para testar

### FIX:

- FieldError at /movements/N/update Unknown field(s) (type) specified for Movement
- Melhorar os updates
- Usar tuplas no service do stock

### NOTE:

- Adicionar validacoes mais rigidas nos filters
- Adicionar mais opções no filter do product
- O Erro de nome do ProductCreate ta hardcoded, tem que fazer mais testes
- Da pra usar select no value do filter (usar js)
- Tenho que ver se e melhor usar messages.error no service ou se devo usar um raise
