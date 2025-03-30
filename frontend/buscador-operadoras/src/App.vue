<template>
  <div class="page">
    <header class="topbar">
      <img src="/logo-intuitive.png" alt="Logo Intuitive Care" class="logo" />
    </header>

    <main class="main">
      <div class="content">
        <h2>Busca de Operadoras</h2>
        <p class="description">
          Digite o nome da operadora para buscar informações com base nos dados da ANS.
        </p>

        <input v-model="termo" @keyup.enter="buscar" placeholder="Ex: Amil, Unimed, Bradesco Saúde..." />
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
      resultados: [],
      loading: false,
      erro: ""
    };
  },
  methods: {
    async buscar() {
      this.loading = true;
      this.resultados = [];
      this.erro = "";

      try {
        const response = await axios.get("http://localhost:8000/buscar", {
          params: { q: this.termo }
        });
        this.resultados = response.data.resultados;
      } catch (err) {
        this.erro = "Erro ao buscar dados.";
      } finally {
        this.loading = false;
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
  max-width: 600px;
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

input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  margin-bottom: 10px;
  border-radius: 10px;
  border: 1px solid #ccc;
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
}

button:hover {
  background-color: #7e5bd7;
}

.result-list {
  margin-top: 30px;
  list-style: none;
  padding: 0;
}

.result-item {
  border-bottom: 1px solid #eee;
  padding: 12px 0;
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