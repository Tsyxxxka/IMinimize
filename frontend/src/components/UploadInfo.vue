<template>
  <!-- <el-steps :active="active" finish-status="success" simple style="margin-top: 20px; margin-bottom: 20px; height: 50px; border-radius: 30px">
    <el-step title="UploadGraph"></el-step>
    <el-step title="Settings"></el-step>
    <el-step title="UI"></el-step>
  </el-steps> -->
  <el-tabs type="border-card" style="height: 900px;">
    <el-tab-pane label="Upload&Settings">
      <Upload @getfile="getfile"></Upload>
      <Settings @getSettings="getSettings" @getNodeInfofile="getNodeInfofile"></Settings>
      <Go @getShowSettings="getShowSettings"></Go>
      <el-button type="primary" style="margin-left: 450px;" @click="passtoBackend" >RUN</el-button>
    </el-tab-pane>
  </el-tabs>
  
  <!-- <div style="margin-top: 50px; height: 400px; margin-left: 80px; ">
    <component :is="compoName" @getfile="getfile" @getSettings="getSettings" />
  </div> -->
  
  <!-- <el-button-group style="margin-left: 600px; margin-top: 200px;">
    <el-button type="primary" @click="next" :disabled="this.active == 2">Next Step</el-button>
    <el-button type="primary" @click="passtoBackend" >RUN</el-button>
  </el-button-group> -->
</template>

<script>
import Upload from './Upload.vue'
import Settings from './Settings.vue'
import Go from './Go.vue'
import axios from "axios"
import { ElMessageBox, ElMessage } from 'element-plus'

export default {
  name: 'UploadInfo',
  components: {
    Upload,
    Settings,
    Go,
  },
  data() {
    return {
      active: 0,
      compoName: 'Upload',
      compo: ['Upload', 'Settings', 'Go'],
      file: '',
      nodeInfoFile: '',
      edgeActivation: '',
      activationModel: '',
      nodeInfo: '',
      source: '',
      tag: '',
      error: '',
      method: '',
      shownodeInfo: '',
      showedgeInfo: ''
    }
  },
  mounted() {
    this.active = 0
    this.compoName = 'Upload'
    this.file = ''
    this.nodeInfoFile = ''
    this.edgeActivation = ''
    this.activationModel = ''
    this.nodeInfo = ''
    this.source = ''
    this.tag = ''
    this.error = ''
    this.method = ''
    this.shownodeInfo = ''
    this.showedgeInfo = ''
  },
  watch: {
    error: "GotoErrorPage"
  },
  methods: {
    next() {
      this.active = this.active + 1;
      this.compoName = this.compo[this.active];
    },
    previous() {
      this.active = this.active - 1;
      this.compoName = this.compo[this.active];
    },
    async passtoBackend() {
      let form = new FormData();
      if (this.file == ''){
        this.error = 'No file UPLOAD.'
        return
      }
      if (this.file.name.split('.')[1] != 'txt'){
        this.error = 'Not Allowed Extension: ' + this.file.name.split('.')[1] + '.'
        return
      }
      form.append("file", this.file);
      if (this.edgeActivation == '') {
        this.error = 'Does your file CONTAINs Edge Activation Probability ?'
      } else if (this.edgeActivation == 'No' && this.activationModel == '') {
        this.error = 'Please choose your activation model if NO edge probability is customized.'
      }
      form.append("edgeActivation", this.edgeActivation);
      form.append("activationModel", this.activationModel)
      if (this.nodeInfo == '') {
        this.error = 'Does your file CONTAINs Supplementary Information for every NODEs ?'
      } else if (this.nodeInfo == 'Yes' && this.nodeInfofile == '') {
        this.error = 'Please upload your Vertex Info FILE.'
      }
      form.append("nodeInfo", this.nodeInfo);
      form.append("nodeInfoFile", this.nodeInfoFile);
      form.append("source", this.source);
      form.append("shownodeInfo", this.shownodeInfo);
      form.append("showedgeInfo", this.showedgeInfo);
      console.info(form)
      const res = await axios.post("http://127.0.0.1:8010/form_rec", form).catch((error)=>{
                        this.showMessage(error.response);
                    });
      console.info(res)
      this.$emit("passFileNameToUI", {'filename': this.file.name, 'methodname': this.method});
    },
    getfile(file) {
      this.file = file 
      console.info(file)
    },
    getNodeInfofile(file){
      this.nodeInfoFile = file
      console.info(file)
    },
    getSettings(form) {
      this.edgeActivation = form['edgeActivation']
      this.activationModel = form['activationModel']
      this.nodeInfo = form['nodeInfo']
      this.source = form['source']
      this.method = form['method']
    },
    getShowSettings(form) {
      this.shownodeInfo = form['shownodeInfo']
      this.showedgeInfo = form['showedgeInfo']
    },
    GotoErrorPage() {
      this.compoName = 'Upload'
      if(this.error == ''){
        return
      }
      this.open()
      this.active = 0
      this.error = ''
    },
    open() {
      ElMessageBox.confirm(
        this.error + ' Please MODIFY your file or settings.',
        'Warning',
        {
          confirmButtonText: 'OK',
          // cancelButtonText: 'Cancel',
          type: 'warning',
          center: true,
        }
      )
        .then(() => {
          ElMessage({
            type: 'info',
            message: 'Upload files and Settings FAILED.',
          })
        })
        //.catch(() => {
        //  ElMessage({
        //    type: 'info',
        //    message: 'Delete canceled',
        //  })
        //})
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style type="text/css">
</style>
