# 打包验证

日期：2026-11-01（Asia/Shanghai）。本文件记录包的可读取性、完整性和离线脚本验证，不代表图片实测通过。

## 复核命令

```powershell
python -B scripts/verify-package.py
python -B skills/huawei-radar-daily-images/scripts/run.py --help
```

原始20项脚本测试保存在 scripts/test-huawei-daily-images.py。19项可在无Git项目中执行；另1项 test_git_output_boundary 需要Git仓库上下文。建议将整个包解压到一次性验证目录，在该目录执行 git init 后再运行：

```powershell
python -B scripts/test-huawei-daily-images.py
```

git init 仅用于测试用副本，不是正常生成的前置条件；不要因此改变既有项目的Git配置。测试用合成Word、位图、审核记录会标识为fixture，不是业务材料和真实imagegen结果。

本次执行结果见同目录 package-check.json 和 offline-tests.txt；最终ZIP另经CRC、逐文件哈希与解压后校验。原工作区没有进行Git提交、部署或覆盖源码。
