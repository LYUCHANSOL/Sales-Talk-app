{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "machine_shape": "hm",
      "gpuType": "L4",
      "authorship_tag": "ABX9TyP2q9PLNAaM5KiZkynAsRAn",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    },
    "accelerator": "GPU"
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/minji0620/sk_broadband/blob/main/Sales%20Talk/%EA%B8%B0%EC%97%85%EC%97%B0%EA%B3%84_Sales_Talk(%EB%8C%80%ED%99%94%ED%98%95).ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import pandas as pd\n",
        "from openai import OpenAI\n",
        "from getpass import getpass\n",
        "\n",
        "# API 키 설정\n",
        "api_key = getpass('OpenAI API 키를 입력하세요: ')\n",
        "client = OpenAI(api_key=api_key)\n",
        "\n",
        "# GPT-4o-mini와 대화하는 함수\n",
        "def chat_with_gpt4omini(prompt, max_tokens=150):\n",
        "    try:\n",
        "        response = client.chat.completions.create(\n",
        "            model=\"gpt-4o-mini\",\n",
        "            messages=[\n",
        "                {\"role\": \"system\", \"content\": \"너는 sk 브로드 밴드 sales 매니저이고 고객에게 iptv를 가입 추천하려는게 목적이야\"},\n",
        "                {\"role\": \"user\", \"content\": prompt}\n",
        "            ],\n",
        "            max_tokens=max_tokens,\n",
        "            temperature=0.01\n",
        "        )\n",
        "        return response.choices[0].message.content.strip()\n",
        "    except Exception as e:\n",
        "        return f\"An error occurred: {str(e)}\"\n",
        "\n",
        "# 고객 특성에 따른 추천 이유 매핑\n",
        "mean1_to_template = {\n",
        "    \"기가인터넷 사용\": \"고속 인터넷을 사용 중이니 IPTV 이용에 적합합니다.\",\n",
        "    \"데이터 사용량 많음\": \"인터넷 사용량이 많은 편이라 IPTV 이용에 적합합니다.\",\n",
        "    \"와이파이 사용\": \"SK 와이파이를 사용 중이시라면 IPTV도 함께 이용하시기 좋아요.\",\n",
        "    \"윙즈 사용\": \"윙즈를 이미 이용 중이라 IPTV 연결도 원활하게 이용 가능합니다.\",\n",
        "    \"장기고객\": \"장기간 이용 고객님께는 IPTV 추가 시 혜택도 더해드립니다.\",\n",
        "    \"재약정함\": \"재약정을 하셨다면 IPTV 추가 시 추가 혜택을 적용받을 수 있습니다.\"\n",
        "}\n",
        "\n",
        "# 프롬프트 생성 함수\n",
        "def build_interactive_prompt(mean1_list, mean2_list):\n",
        "    # 알파벳(혹은 원하는 기준) 순으로 정렬\n",
        "    mean1_list_sorted = sorted(mean1_list)\n",
        "    mean2_list_sorted = [mean1_to_template.get(k, \"적합한 추천 이유\") for k in mean1_list_sorted]\n",
        "\n",
        "    mean1_str = \"\\n- \" + \"\\n- \".join(mean1_list_sorted)\n",
        "    mean2_str = \"\\n- \" + \"\\n- \".join(mean2_list_sorted)\n",
        "\n",
        "    return f\"\"\"\n",
        "고객 특성:{mean1_str}\n",
        "\n",
        "추천 근거:{mean2_str}\n",
        "\n",
        "- 친절하지만 전문가답고, 과하게 영업티는 나지 않게 해줘.\n",
        "- 반드시 추천 근거만 활용하고, 가족, 여가, 취향 등 추가적인 부가 설명은 넣지 마.\n",
        "- 입력된 특성을 반복해서 언급하지 말고, 중복된 내용은 한 번만 언급해.\n",
        "- 문장은 간결하게, 2문장 이내로 작성해.\n",
        "- 반드시 고객의 특성과 추천 이유 내에 명시된 내용만 활용해 문장을 작성할 것\n",
        "- 입력한 고객 특성을 모두 사용해 줘\n",
        "\"\"\"\n",
        "\n",
        "\n",
        "# 사용자 입력 반복 받기\n",
        "def run_interactive_mode():\n",
        "    print(\"\\n고객 특성을 입력하세요 (쉼표로 구분, 예: 데이터 사용량 많음, 기가인터넷 사용)\")\n",
        "    print(\"'끝'을 입력하면 종료됩니다.\\n\")\n",
        "\n",
        "    while True:\n",
        "        user_input = input(\"고객 특성 입력: \").strip()\n",
        "\n",
        "        if user_input.lower() == \"끝\":\n",
        "            print(\"프로그램을 종료합니다.\")\n",
        "            break\n",
        "\n",
        "        mean1_list = [x.strip() for x in user_input.split(\",\")]\n",
        "        mean2_list = [mean1_to_template.get(k, \"적합한 추천 이유\") for k in mean1_list]\n",
        "        prompt = build_interactive_prompt(mean1_list, mean2_list)\n",
        "        response = chat_with_gpt4omini(prompt)\n",
        "\n",
        "        print(\"\\n[Sales Talk]\")\n",
        "        print(response)\n",
        "        print(\"-\" * 60)\n",
        "\n",
        "# 메인 실행\n",
        "if __name__ == \"__main__\":\n",
        "    run_interactive_mode()\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "eLPRKdOl09aB",
        "outputId": "81955c66-cb96-4f24-93c1-cf571e860a8f"
      },
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "OpenAI API 키를 입력하세요: ··········\n",
            "\n",
            "고객 특성을 입력하세요 (쉼표로 구분, 예: 데이터 사용량 많음, 기가인터넷 사용)\n",
            "'끝'을 입력하면 종료됩니다.\n",
            "\n",
            "고객 특성 입력: 와이파이 사용, 윙즈 사용, 데이터 사용량 많음\n",
            "\n",
            "[Sales Talk]\n",
            "고객님은 데이터 사용량이 많으시고 SK 와이파이를 이용 중이시므로 IPTV 이용에 적합합니다. 또한, 윙즈를 사용하고 계시기 때문에 IPTV 연결도 원활하게 이용하실 수 있습니다.\n",
            "------------------------------------------------------------\n",
            "고객 특성 입력: 와이파이 사용, 재약정 함, 데이터 사용량 많음\n",
            "\n",
            "[Sales Talk]\n",
            "고객님은 데이터 사용량이 많으시고 SK 와이파이를 이용 중이시므로 IPTV 이용에 적합합니다. 재약정 하신 만큼 IPTV와 함께 더 나은 인터넷 환경을 경험하실 수 있습니다.\n",
            "------------------------------------------------------------\n",
            "고객 특성 입력: 재약정 함, 와이파이 사용, 데이터 사용량 많음\n",
            "\n",
            "[Sales Talk]\n",
            "고객님은 데이터 사용량이 많으시고 SK 와이파이를 이용 중이시므로 IPTV 이용에 적합합니다. 재약정 하신 만큼 IPTV와 함께 더 나은 인터넷 환경을 경험하실 수 있습니다.\n",
            "------------------------------------------------------------\n",
            "고객 특성 입력: 윙즈 사용, 와이파이 사용, 데이터 사용량 많음\n",
            "\n",
            "[Sales Talk]\n",
            "고객님은 데이터 사용량이 많으시고 SK 와이파이를 이용 중이시므로 IPTV 이용에 적합합니다. 또한, 윙즈를 사용하고 계시기 때문에 IPTV 연결도 원활하게 이루어질 것입니다.\n",
            "------------------------------------------------------------\n",
            "고객 특성 입력: 끝\n",
            "프로그램을 종료합니다.\n"
          ]
        }
      ]
    }
  ]
}
