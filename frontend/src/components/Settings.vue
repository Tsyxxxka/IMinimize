<template>
  <!-- <el-tabs type="border-card" style="width: 1000px; height: 700px; border-radius: 30px" v-model="form.method">
    <el-tab-pane label="Min" name="Min"> -->
    <el-form 
      :model="form" 
      style="margin-left: 230px;"
      class="elformclass">
      <el-tooltip content="Do you have edge activation probability in your file?" placement="top">
        <el-form-item label="Edge Activation Probability">
          <el-radio-group v-model="form.edgeActivation" style="margin-left:60px">
            <el-radio label="Yes" name="type">Yes</el-radio>
            <el-radio label="No" name="type">No</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-tooltip>
      <el-form-item label="Choose Edge Activation Model" v-if="form.edgeActivation=='No'">
        <el-radio-group v-model="form.activationModel" style="margin-left:25px">
          <el-radio label="WC" name="type">WC</el-radio>
          <el-radio label="TR" name="type">TR</el-radio>
        </el-radio-group>
      </el-form-item>
        
      <el-tooltip content="Do you have supplementary info for each vertex in your file?" placement="top">
        <el-form-item label="Supplementary Vertex Info">
          <el-radio-group v-model="form.nodeInfo" style="margin-left:68px">
            <el-radio label="Yes"></el-radio>
            <el-radio label="No"></el-radio>
          </el-radio-group>
        </el-form-item>
      </el-tooltip>
      <div v-if="form.nodeInfo=='Yes'">
      <el-form-item>
        <el-upload
          drag
          action="action"
          :http-request="goto"
          multiple
          style="margin-left: 180px;">
          <!-- <i class="el-icon-upload"></i> -->
          <div class="el-upload__text">Drag files here, or <em> click here Upload</em></div>
        </el-upload>
      </el-form-item>
      </div>

      <el-form-item label="Seed Vertices">
        <el-input 
        type="textarea" 
        v-model="form.source" 
        style="width: 340px;" 
        placeholder="Please enter your seed vertices' id separated by space, e.g. '0 1' ">
        </el-input>
      </el-form-item>
    </el-form>
    <!-- </el-tab-pane>
    <el-tab-pane label="Max" name="Max"> -->
      <!-- <el-form 
      :model="form" 
      label-width="300px" 
      style="height: 600px; margin-top: 70px; margin-left: 150px;"
      class="elformclass">

      <el-tooltip content="Has edge activation probability in your file?" placement="top">
        <el-form-item label="Edge Activation Probability">
          <el-radio-group v-model="form.edgeActivation">
            <el-radio label="Yes" name="type"></el-radio>
            <el-radio label="No" name="type"></el-radio>
          </el-radio-group>
        </el-form-item>
      </el-tooltip>

      <el-tooltip content="Has supplementary info for each node in your file?" placement="top">
        <el-form-item label="Supplementary Information">
          <el-radio-group v-model="form.nodeInfo">
            <el-radio label="Yes"></el-radio>
            <el-radio label="No"></el-radio>
          </el-radio-group>
        </el-form-item>
      </el-tooltip>
        
      </el-form>
    </el-tab-pane>
  </el-tabs> -->

</template>

<script>
export default {
  name: 'Settings',
  data() {
    return {
      form: {
        edgeActivation: '',
        activationModel: '',
        nodeInfo: '',
        source: '',
        method: 'Min',
      }
    }
  },
  watch: {
    form:{
      handler() {
        this.uploadSettings()
      },
      deep: true
    }
  },
  methods: {
    uploadSettings () {
      this.$emit("getSettings", this.form)
    },
    goto(params) {
      this.$emit('getNodeInfofile',params.file)
    }
  }
}
</script>

<style>
.elformclass .el-form-item__label {
  font-size: 20px;
  color: #335A66;
}
.el-radio-group {
  margin-left: 50px;
}

</style>

<style scoped>
.el-radio /deep/ .el-radio__label {
  font-size: 20px;
  color: #335A66;
}


</style>

<style scoped>
/deep/ .el-upload{
  width: 340px;
  height: 40px;
}
/deep/ .el-upload .el-upload-dragger{
  width: 340px;
  height: 40px;
}
</style>