<template>
  <el-form class="elformclass" label-width="200px" style="margin-left: 165px; margin-top: 10px;">
    <el-form-item label="Upload Graph" >
      <el-upload
        drag
        action="action"
        :http-request="goto"
        multiple>
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">Drag files here, or <em> click here Upload</em></div>
      </el-upload>
    </el-form-item>
  </el-form>
</template>



<script>  
export default {
  name: 'Upload',
  methods: {
    goto(params) {
      this.$emit('getfile',params.file)
    }
  }
}
</script>

<style>
.elformclass .el-form-item__label {
  font-size: 20px;
  color: #335A66;
  margin-right: 50px;
}

</style>

<style scoped>
/deep/ .el-upload{
  width: 340px;
  height: 180px;
}
/deep/ .el-upload .el-upload-dragger{
  width: 340px;
  height: 180px;
}
</style>