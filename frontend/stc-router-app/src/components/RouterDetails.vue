<template>
  <div>
    <h2 class="head_center">{{ router.name }}</h2>
    <el-main>
      <el-alert type="warning">
        <p> expand row for more info about port staus</p>
      </el-alert>

      <span class="badge-up badge-success">up</span>
      <span class="badge-down badge-danger">down</span>
      <el-table
        :data="slots"
        style="width: 100%">
        <el-table-column type="expand">
          <template slot-scope="props">
           <span v-for=" port in props.row.ports" :key="port.id"
                 class="badge"
                 v-on:click="remoteRouter(port.remote_router)"
                 v-bind:class="{ 'badge-success' : port.state.toLowerCase() === 'up', 'badge-danger': port.state.toLowerCase() === 'down' ||  port.state.toLowerCase() === 'shutdown' }">
            {{port.name}}
          </span>
          </template>
        </el-table-column>
        <el-table-column
          label="slot interface"
          prop="name">
        </el-table-column>
        <el-table-column
          label="slot name"
          prop="node_type">
        </el-table-column>
        <el-table-column
          label="total ports"
          prop="port_count">
        </el-table-column>
        <el-table-column
          label="speed"
          prop="speed">
        </el-table-column>
        <el-table-column
          label="state"
          prop="state">
        </el-table-column>
      </el-table>
    </el-main>
  </div>
</template>
<script>
  import {API_ROOT} from '../env_variables';
  export default {
    name: 'RouterDetails',

    data() {
      return {
        slots: [],
        router: {
          name: '',
          id: ''
        }
      }
    },

    created() {
      this.fetchData()
    },

    watch: {
      '$route': 'fetchData'
    },

    methods: {
      remoteRouter(router){
        debugger;
        if (router) {
          this.$router.push({name: 'router-details', params: {id: router[0].id}})
        } else {
          this.$message.error('Oops, this is not STC router. kindly select red routers');
        }
      },
      fetchData() {
        this.$http.get(API_ROOT + 'slot/?router=' + this.$route.params.id)
          .then((resp) => {
            this.slots = resp.data;
            this.router = resp.data[0].router;
            console.log(resp)
          })
          .catch((err) => {
            console.log(err)
          })
      }
    }
  }
</script>
