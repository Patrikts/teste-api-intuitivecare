<template>
  <div class="container">
    <h1>Busca de Operadoras - ANS</h1>

    <input v-model="termo" @keyup.enter="buscar" placeholder="Digite a razão social..." />
    <button @click="buscar">Buscar</button>

    <div v-if="loading">Buscando...</div>

    <div v-if="resultados.length">
      <h2>Resultados:</h2>
      <ul>
        <li v-for="(item, index) in resultados" :key="index">
          <strong>{{ item.razao_social }}</strong><br />
          Registro ANS: {{ item.registro_ans }}<br />
          CNPJ: {{ item.cnpj }}<br />
          UF: {{ item.uf }} | Município: {{ item.municipio }}<br />
          Similaridade: {{ item.pontuacao }}%
        </li>
      </ul>
    </div>

    <div v-if="erro">{{ erro }}</div>
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

<style>
.container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}
input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
}
button {
  padding: 8px 12px;
}
li {
  margin-bottom: 12px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
}
</style>
