# WK08 Lab: ML Pipeline & AI Agent Integration

## 📋 Project Overview
โปรเจกต์นี้เป็นการสร้างกระบวนการทำ Machine Learning แบบมาตรฐาน (Standardized Workflow) และใช้ AI Agent ในการวิเคราะห์ประสิทธิภาพของโมเดลโดยอัตโนมัติ

## 🧪 Lab Parts
1. **Part 1:** Standardizing the ML Workflow โดยใช้ Scikit-Learn Pipeline
2. **Part 2:** Rapid Prototyping โดยใช้ PyCaret (หรือ Scikit-Learn แทนสำหรับ Python 3.12+)

## 🤖 AI Model Analysis Result (from pycaretflow.py)
> **Agent Analysis:** > จากผลการทดสอบด้วยโมเดล Random Forest ที่ได้ค่า Accuracy **0.9012** และ F1-Score **0.8845** > ทางระบบ AI Agent ให้ความเห็นว่าโมเดลมีความพร้อมในการใช้งาน (Deployment) ในระดับทดสอบ 
> แต่มีความเสี่ยงในเรื่องของ Bias ต่อกลุ่มข้อมูลที่มีปริมาณมากเกินไป (Majority Class) 
> ควรมีการปรับสมดุลข้อมูลก่อนใช้งานในระบบ Production จริง

## 🛠️ MCP Server Integration
โครงการนี้มี `pycaret-mcp-server` สำหรับให้ AI (เช่น Claude หรือ GPT) สามารถเรียกใช้เครื่องมือ ML ผ่าน Protocol ได้