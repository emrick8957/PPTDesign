# C5 交付打包提示词

你是角色 C。现在将页面图片、报告和 manifest 打包为标准交付目录。

## 目录

```text
deliverables/
├── page_images/
│   ├── P01_*.png
│   └── ...
├── previews/
│   └── contact_sheet.png
├── reports/
│   ├── self_check_report.md
│   └── optimization_report.md
│   └── C2_6_optimization_report.md
├── delivery_manifest.json
└── delivery.zip
```

## manifest 必填字段

- project_name
- delivery_mode
- page_range
- image_resolution
- source_files
- generated_files
- self_check_summary
- known_limitations
- created_at

## 交付回复

回复用户时只列出：

- ZIP 下载链接；
- contact sheet 链接；
- 自检报告链接；
- 单页图片链接。

不要重复长篇报告正文，除非用户要求。
