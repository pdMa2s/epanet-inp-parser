const express = require('express')
const entrypoint = __dirname + '/index.html'
const app = express()
const port = 5000

app.get('/', (req, res) => {
  res.sendFile(entrypoint)
})

app.use('/static', express.static('static'))

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})