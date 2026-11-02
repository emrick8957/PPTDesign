# 华为风格 PPT 图片 Skill 项目

打包日期：2026-11-01（Asia/Shanghai）。项目适配版本：1.2.0。

这是本次对话所用主工作区优化版的完整项目快照，保留源码和固定资源原始字节。它包含可复用工作流与脚本，需要由具备工具能力的 AI 宿主执行，不是双击后自动出图的应用程序。

## 开始使用

1. 完整解压 ZIP，打开解压后的项目根目录。不要只取出 SKILL.md 或移动其下的 vendor 文件。
2. 让执行助手读取本目录 AGENTS.md 和下述入口；从 `通用提示词.md` 复制所需模板，替换 `{项目根目录}`、`{Word绝对路径}`、`{日期}` 等变量。占位符不应出现在成品中。
3. 优先使用“日报 Step1 / Step2”两条提示词；若希望一次执行到底，使用明确覆盖默认阶段停点的“日报连续执行”提示词。模板文件本身不是任务授权，只有用户实际发送的内容才构成指令。
4. 首次先执行依赖校验，再开始真实材料读取。

```powershell
# 在项目根目录执行；python 应指向已具备 Pillow 的 Python 3.10+。
python -B scripts/verify-package.py
python -B skills/huawei-radar-daily-images/scripts/run.py verify
python -B skills/huawei-radar-daily-images/scripts/run.py --help
```

`verify-package.py` 检查包内清单、必读材料、原包哈希与 Pillow；不会调用模型，不证明材料已经被读懂。若环境没有 Pillow，可按宿主已有依赖管理方式安装 requirements.txt；本包不会自行安装依赖。

## 环境要求

- 本地文件读写、Python 3.10+、Pillow。
- 能阅读原文网页或 PDF 的工具；无法访问的来源必须注明并排除无依据断言。
- 内置 imagegen 和本地看图能力。模型、账户、图像生成服务及密钥不在包内，脚本不直接调用模型，也没有付费 API 后备。
- 真正独立的审核 Agent。日报正式交付需要独立审核；无法提供时停在待审核状态。
- 普通使用不要求 Git、PowerPoint、OpenClaw 或原作者电脑的目录。若执行原始测试套件的 Git 边界用例，需要 Git，见 `docs/verification.md`。

## 入口与目录

| 内容 | 位置 |
| --- | --- |
| 优化版日报入口 | skills/huawei-radar-daily-images/SKILL.md |
| 项目发现别名 | .agents/skills/radar-daily-images/SKILL.md |
| 两阶段、阅读清单、视觉合同、审核规则 | skills/huawei-radar-daily-images/references/ |
| 状态、校验、归一、审核绑定、交付脚本 | skills/huawei-radar-daily-images/scripts/run.py |
| Master / Builder | skills/huawei-radar-daily-images/vendor/upstream/bundle/skills0818-20260912/ |
| 原始 skills0818.zip | skills/huawei-radar-daily-images/vendor/upstream/source/skills0818.zip |
| Golden Style ZIP | 上述 bundle 下 huawei_ppt_builder/templates/Golden_Style.zip |
| Golden P1–P10 | 上述 bundle 下 golden_reference/Golden_Style/style1/ |
| 可复制提示词 | 通用提示词.md |
| 本次打包验证和已知限制 | docs/verification.md、docs/known-limitations.md |
| 逐文件 SHA-256 | package-manifest.json |

日报运行器固定使用十页 Word 日报精读：1920×1080 PNG、technical_deep_dive、逐页内联预览，不生成 PPTX。通用主题模板使用上游 Master / Builder，其页数和品牌可由用户指定，尚不具备日报运行器的同等状态自动化；不可把更改提示词当作已改造了固定十页脚本。

原包中的历史工作区路径按来源记录保留；日报实际路径由项目适配层覆盖到本包 reports/daily-images。不要修改锁文件或替换同名资产以消除历史路径。

## 版本与验收状态

本次仅打包和核验，没有再生成图片，也没有继续修改 Skill 机制。133 个锁定资源及项目入口按原字节保留。

上一轮图片验证反馈仍有公共区位置与红色焦点问题；详见已知限制。这是可复用的验证版项目快照，不是“严格视觉验收已通过”的版本。离线测试、ZIP 完整性和真实图片质量是不同证据。

包中不含业务日报 Word、历史任务运行目录或上轮生成样张；Golden Style 和上游回归样例是 Skill 固定依赖，已保留。没有打包个人环境、凭据或整个雷达业务仓库。
