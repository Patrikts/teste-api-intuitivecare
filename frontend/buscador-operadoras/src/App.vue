<template>
  <div class="page">
    <header class="topbar">
      <img src="./assets/logo-intuitive-care.jpg" alt="Logo Intuitive Care" class="logo" />
    </header>

    <main class="main">
      <div class="content">
        <h2>Busca de Operadoras</h2>
        <p class="description">
          Digite o nome da operadora para buscar informações com base nos dados da ANS.
        </p>

        <input v-model="termo" placeholder="Nome, fantasia ou CNPJ..." />
        <div class="filters">
          <select v-model="uf">
            <option value="">UF (opcional)</option>
            <option v-for="estado in ufs" :key="estado" :value="estado">{{ estado }}</option>
          </select>

          <input v-model="cidade" placeholder="Cidade (opcional)" />
        </div>

        <button @click="buscar">Buscar</button>

        <div v-if="loading" class="loading">Buscando...</div>

        <ul v-if="resultados.length" class="result-list">
          <li v-for="(item, index) in resultados" :key="index" class="result-item">
            <h3>{{ item.razao_social }}</h3>
            <p><strong>Registro ANS:</strong> {{ item.registro_ans }}</p>
            <p><strong>CNPJ:</strong> {{ item.cnpj }}</p>
            <p><strong>UF:</strong> {{ item.uf }} | <strong>Município:</strong> {{ item.municipio }}</p>
            <p><strong>Similaridade:</strong> {{ item.pontuacao }}%</p>
          </li>
        </ul>

        <div v-if="resultados.length" class="pagination">
          <button @click="anterior" :disabled="pagina === 1">Anterior</button>
          <span>Página {{ pagina }}</span>
          <button @click="proxima" :disabled="pagina * limite >= total">Próxima</button>
        </div>

        <div v-if="erro" class="error">{{ erro }}</div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      termo: "",
      uf: "",
      cidade: "",
      resultados: [],
      pagina: 1,
      limite: 5,
      total: 0,
      loading: false,
      erro: "",
      ufs: [
        "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO",
        "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR",
        "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"
      ]
    };
  },
  methods: {
    async buscar() {
      this.loading = true;
      this.resultados = [];
      this.erro = "";

      try {
        const response = await axios.get("http://localhost:8000/buscar", {
          params: {
            q: this.termo,
            uf: this.uf || undefined,
            cidade: this.cidade || undefined,
            page: this.pagina,
            limit: this.limite
          }
        });

        this.resultados = response.data.resultados;
        this.total = response.data.total_encontrado;
      } catch (err) {
        this.erro = "Erro ao buscar dados.";
      } finally {
        this.loading = false;
      }
    },
    anterior() {
      if (this.pagina > 1) {
        this.pagina--;
        this.buscar();
      }
    },
    proxima() {
      if (this.pagina * this.limite < this.total) {
        this.pagina++;
        this.buscar();
      }
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700&display=swap');

.page {
  font-family: 'Montserrat', sans-serif;
  color: #111;
  background-color: #fff;
  min-height: 100vh;
}

.topbar {
  padding: 20px 40px;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
}

.logo {
  height: 36px;
}

.main {
  display: flex;
  justify-content: center;
  padding: 60px 20px;
}

.content {
  max-width: 700px;
  width: 100%;
}

h2 {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 10px;
}

.description {
  font-size: 16px;
  color: #444;
  margin-bottom: 30px;
}

input, select {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  margin-bottom: 10px;
  border-radius: 10px;
  border: 1px solid #ccc;
}

.filters {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filters select, .filters input {
  flex: 1;
  min-width: 150px;
}

button {
  background-color: #a678e2;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-weight: bold;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.3s ease;
  margin-bottom: 20px;
}

button:hover {
  background-color: #7e5bd7;
}

.result-list {
  list-style: none;
  padding: 0;
}

.result-item {
  border-bottom: 1px solid #eee;
  padding: 12px 0;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.loading {
  margin-top: 10px;
  color: #555;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
