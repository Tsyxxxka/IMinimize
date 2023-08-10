<template>
  <el-container>
    <el-aside width="250px">
      <div style="height: 100%; text-align: left;">
        <el-menu
        
          default-active="activePage"
          class="el-menu-vertical-demo"
          background-color="#17393B"
          text-color="#D7CCC8"
          active-text-color="#fff"
          style="height: 100%">
          
          <el-menu-item @click="changePageTo('HomePage')" :index="1">
            <i class="el-icon-document" style="font-size: 25px; margin-right: 10px"></i>
            <span>Home</span>
          </el-menu-item>

          <el-menu-item @click="changePageTo('UploadInfo')" :index="2">
            <i class="el-icon-setting" style="font-size: 25px; margin-right: 10px"></i>
            <span>Upload</span>
          </el-menu-item>
          
          <el-menu-item @click="changePageTo('GraphCanvas')" :index="3">
            <i class="el-icon-menu" style="font-size: 25px; margin-right: 10px"></i>
            <span>Visualization</span>
          </el-menu-item>

          <!-- <el-menu-item :index="4">
            <i class="el-icon-setting" style="font-size: 25px; margin-right: 10px"></i>
            <span>Database</span>
          </el-menu-item> -->

        </el-menu>
      </div>
    </el-aside>

    <el-container>
      <el-main>
        <component 
          :is="comName" 
          @passFileNameToUI="getFileName" 
          :fileName="fileName"
          :minOrmax="methodName"
          >
        </component>
      </el-main>
    </el-container>

  </el-container>
</template>

<script>
import HomePage from './HomePage.vue'
import UploadInfo from './UploadInfo.vue'
import GraphCanvas from './GraphCanvas.vue'

export default {
  name: 'MainPage',
  data() {
    return {
      comName: 'HomePage',
      fileName: '',
      methodName: 'Min',
      activePage: '1'
    }
  },
  components: {
    HomePage,
    UploadInfo,
    GraphCanvas,
  },
  methods: {
    changePageTo(info) {
      this.comName = info
    },
    getFileName(UIdata) {
      this.fileName = UIdata['filename']
      this.methodName = UIdata['methodname']
      
      // this.comName = 'GraphCanvas'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped type="text/css">
  span {
    font-size: 20px;
  }

  .el-menu-item {
    margin-top: 40px;
    margin-left: 40px;
    margin-right: 40px;
  }

  .el-button {
    font-family: Arial;
    font-size: 25px;
  }

  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }
  
  .el-main {
    /* background-color: #D7CCC8; */
    color: #333;
    height: 1000px;
  }

  body > .el-container {
    margin-bottom: 40px;
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
