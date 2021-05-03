{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Project.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/TcgVanguardTroll/CSE-467-QA/blob/main/Project.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "qd9pHZeDbDEx"
      },
      "source": [
        "ll"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 749
        },
        "id": "xxEo0gtnURDs",
        "outputId": "4798396e-c68b-4dd4-b7d8-88d1a4817e43"
      },
      "source": [
        "import nltk\n",
        "import re\n",
        "import os\n",
        "nltk.download('punkt')\n",
        "nltk.download('averaged_perceptron_tagger')\n",
        "nltk.download('wordnet')\n",
        "from nltk.corpus import wordnet\n",
        "from nltk.parse import stanford\n",
        "from functools import * \n",
        "\n",
        "# !wget 'https://nlp.stanford.edu/software/stanford-tagger-4.2.0.zip'\n",
        "# !unzip 'stanford-tagger-4.2.0.zip'\n",
        "\n",
        "# jar = '/content/stanford-postagger-4.2.0'\n",
        "# model = '/content/stanford-postagger-full-2020-11-17/models/english-left3words-distsim.tagger'\n",
        "\n",
        "\n",
        "# stanford_tagger = StanfordPOSTagger(model, jar, encoding='utf8')\n",
        "\n",
        "\n",
        "from nltk.tag.stanford import CoreNLPPOSTagger, CoreNLPNERTagger\n",
        "from nltk.parse.corenlp import CoreNLPParser\n",
        "stpos, stner = CoreNLPPOSTagger(), CoreNLPNERTagger()\n",
        "# stpos.tag('What is the airspeed of an unladen swallow ?'.split())\n",
        "\n",
        "who_query = []\n",
        "yes_no_query = []\n",
        "declaration_query = []\n",
        "\n",
        "#def determine_type(sentence):\n",
        "# return \n",
        "\n",
        "# def declare(declaration):\n",
        "#   return  \n",
        "# def yes_no_question(question):\n",
        "#   return\n",
        "# def who(question):\n",
        "#   return\n",
        "\n",
        "def tokenize(words):\n",
        "  raw_tokens =  list(filter(lambda x: re.match(r\"[A-Za-z]\",x),nltk.word_tokenize(words)))\n",
        "  \n",
        "  tagged = nltk.pos_tag(raw_tokens) \n",
        "\n",
        "  type_map = {'J':wordnet.ADJ,'V':wordnet.VERB,'N':wordnet.NOUN,'R':wordnet.ADV,'D':wordnet.NOUN}\n",
        "  lemma =  nltk.stem.WordNetLemmatizer()\n",
        "  return [\n",
        "      (lemma.lemmatize(token,type_map[type_value[0]]),type_value) if type_value[0] in type_map\n",
        "      else lemma.lemmatize(token) \n",
        "      for token,type_value in tagged\n",
        "    ]\n",
        "\n",
        "def create_dict(words):\n",
        "  type_dict= { wordnet:[] for word, word_type in words }\n",
        "  for word,word_type in words:\n",
        "      type_dict[word_type].append(word) \n",
        "  return type_dict\n",
        "\n",
        "def parse(words):\n",
        "  grammer_str = \"\"\"\n",
        "      # % start S\n",
        "      ############################\n",
        "      # Grammar rules\n",
        "      ############################\n",
        "        S -> NP VP\n",
        "        PP -> P NP\n",
        "        NP -> DT N\n",
        "        N -> N PP\n",
        "        N -> Adj N\n",
        "        VP -> IV\n",
        "        VP -> TV NP\n",
        "        VP -> DTV NP NP\n",
        "        VP -> DTV NP PP\n",
        "        VP -> VP PP\n",
        "        VP -> SV S\n",
        "        VP -> AUX VP\n",
        "        VP -> ADV VP  \n",
        "        NP -> PN\n",
        "        NP -> PRN\n",
        "      ############################ \n",
        "\"\"\"\n",
        "  wordtype_dict = create_dict(words)\n",
        "  \n",
        "  pls= lambda ls: reduce(lambda type_value,string: string+\" \"+type_value+\"\\n\" ,ls,\"\")  \n",
        "\n",
        "  pk = lambda str_value:str_value+\" ->\"\n",
        "\n",
        "  rules= [  pk(k) + pls(ls)  for k,ls in wordtype_dict.items()]\n",
        "  \n",
        "  \n",
        "\n",
        "  my_grammar = nltk.CFG.fromstring(string)\n",
        " \n",
        "  \n",
        "\n",
        "\n",
        "tokenize(\"A man entered the dealership.\")\n",
        "determine_type(\"A man entered the dealership.\")"
      ],
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "[nltk_data] Downloading package punkt to /root/nltk_data...\n",
            "[nltk_data]   Unzipping tokenizers/punkt.zip.\n",
            "[nltk_data] Downloading package averaged_perceptron_tagger to\n",
            "[nltk_data]     /root/nltk_data...\n",
            "[nltk_data]   Unzipping taggers/averaged_perceptron_tagger.zip.\n",
            "[nltk_data] Downloading package wordnet to /root/nltk_data...\n",
            "[nltk_data]   Unzipping corpora/wordnet.zip.\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "error",
          "ename": "ConnectionError",
          "evalue": "ignored",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mConnectionRefusedError\u001b[0m                    Traceback (most recent call last)",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/connection.py\u001b[0m in \u001b[0;36m_new_conn\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m    158\u001b[0m             conn = connection.create_connection(\n\u001b[0;32m--> 159\u001b[0;31m                 (self._dns_host, self.port), self.timeout, **extra_kw)\n\u001b[0m\u001b[1;32m    160\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/util/connection.py\u001b[0m in \u001b[0;36mcreate_connection\u001b[0;34m(address, timeout, source_address, socket_options)\u001b[0m\n\u001b[1;32m     79\u001b[0m     \u001b[0;32mif\u001b[0m \u001b[0merr\u001b[0m \u001b[0;32mis\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 80\u001b[0;31m         \u001b[0;32mraise\u001b[0m \u001b[0merr\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     81\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/util/connection.py\u001b[0m in \u001b[0;36mcreate_connection\u001b[0;34m(address, timeout, source_address, socket_options)\u001b[0m\n\u001b[1;32m     69\u001b[0m                 \u001b[0msock\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mbind\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0msource_address\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 70\u001b[0;31m             \u001b[0msock\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mconnect\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0msa\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     71\u001b[0m             \u001b[0;32mreturn\u001b[0m \u001b[0msock\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mConnectionRefusedError\u001b[0m: [Errno 111] Connection refused",
            "\nDuring handling of the above exception, another exception occurred:\n",
            "\u001b[0;31mNewConnectionError\u001b[0m                        Traceback (most recent call last)",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/connectionpool.py\u001b[0m in \u001b[0;36murlopen\u001b[0;34m(self, method, url, body, headers, retries, redirect, assert_same_host, timeout, pool_timeout, release_conn, chunked, body_pos, **response_kw)\u001b[0m\n\u001b[1;32m    599\u001b[0m                                                   \u001b[0mbody\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mbody\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mheaders\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mheaders\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 600\u001b[0;31m                                                   chunked=chunked)\n\u001b[0m\u001b[1;32m    601\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/connectionpool.py\u001b[0m in \u001b[0;36m_make_request\u001b[0;34m(self, conn, method, url, timeout, chunked, **httplib_request_kw)\u001b[0m\n\u001b[1;32m    353\u001b[0m         \u001b[0;32melse\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 354\u001b[0;31m             \u001b[0mconn\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mrequest\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mmethod\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0murl\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mhttplib_request_kw\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    355\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/lib/python3.7/http/client.py\u001b[0m in \u001b[0;36mrequest\u001b[0;34m(self, method, url, body, headers, encode_chunked)\u001b[0m\n\u001b[1;32m   1276\u001b[0m         \u001b[0;34m\"\"\"Send a complete request to the server.\"\"\"\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1277\u001b[0;31m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_send_request\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mmethod\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0murl\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mbody\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mheaders\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mencode_chunked\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1278\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/lib/python3.7/http/client.py\u001b[0m in \u001b[0;36m_send_request\u001b[0;34m(self, method, url, body, headers, encode_chunked)\u001b[0m\n\u001b[1;32m   1322\u001b[0m             \u001b[0mbody\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0m_encode\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mbody\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m'body'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1323\u001b[0;31m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mendheaders\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mbody\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mencode_chunked\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mencode_chunked\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1324\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/lib/python3.7/http/client.py\u001b[0m in \u001b[0;36mendheaders\u001b[0;34m(self, message_body, encode_chunked)\u001b[0m\n\u001b[1;32m   1271\u001b[0m             \u001b[0;32mraise\u001b[0m \u001b[0mCannotSendHeader\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1272\u001b[0;31m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_send_output\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mmessage_body\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mencode_chunked\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mencode_chunked\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1273\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/lib/python3.7/http/client.py\u001b[0m in \u001b[0;36m_send_output\u001b[0;34m(self, message_body, encode_chunked)\u001b[0m\n\u001b[1;32m   1031\u001b[0m         \u001b[0;32mdel\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_buffer\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1032\u001b[0;31m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msend\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mmsg\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1033\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/lib/python3.7/http/client.py\u001b[0m in \u001b[0;36msend\u001b[0;34m(self, data)\u001b[0m\n\u001b[1;32m    971\u001b[0m             \u001b[0;32mif\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mauto_open\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 972\u001b[0;31m                 \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mconnect\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    973\u001b[0m             \u001b[0;32melse\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/connection.py\u001b[0m in \u001b[0;36mconnect\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m    180\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0mconnect\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 181\u001b[0;31m         \u001b[0mconn\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_new_conn\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    182\u001b[0m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_prepare_conn\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mconn\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/connection.py\u001b[0m in \u001b[0;36m_new_conn\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m    167\u001b[0m             raise NewConnectionError(\n\u001b[0;32m--> 168\u001b[0;31m                 self, \"Failed to establish a new connection: %s\" % e)\n\u001b[0m\u001b[1;32m    169\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mNewConnectionError\u001b[0m: <urllib3.connection.HTTPConnection object at 0x7f09afea0f10>: Failed to establish a new connection: [Errno 111] Connection refused",
            "\nDuring handling of the above exception, another exception occurred:\n",
            "\u001b[0;31mMaxRetryError\u001b[0m                             Traceback (most recent call last)",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/requests/adapters.py\u001b[0m in \u001b[0;36msend\u001b[0;34m(self, request, stream, timeout, verify, cert, proxies)\u001b[0m\n\u001b[1;32m    448\u001b[0m                     \u001b[0mretries\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mmax_retries\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 449\u001b[0;31m                     \u001b[0mtimeout\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mtimeout\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    450\u001b[0m                 )\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/connectionpool.py\u001b[0m in \u001b[0;36murlopen\u001b[0;34m(self, method, url, body, headers, retries, redirect, assert_same_host, timeout, pool_timeout, release_conn, chunked, body_pos, **response_kw)\u001b[0m\n\u001b[1;32m    637\u001b[0m             retries = retries.increment(method, url, error=e, _pool=self,\n\u001b[0;32m--> 638\u001b[0;31m                                         _stacktrace=sys.exc_info()[2])\n\u001b[0m\u001b[1;32m    639\u001b[0m             \u001b[0mretries\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msleep\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/util/retry.py\u001b[0m in \u001b[0;36mincrement\u001b[0;34m(self, method, url, response, error, _pool, _stacktrace)\u001b[0m\n\u001b[1;32m    398\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0mnew_retry\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mis_exhausted\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 399\u001b[0;31m             \u001b[0;32mraise\u001b[0m \u001b[0mMaxRetryError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0m_pool\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0murl\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0merror\u001b[0m \u001b[0;32mor\u001b[0m \u001b[0mResponseError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcause\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    400\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mMaxRetryError\u001b[0m: HTTPConnectionPool(host='localhost', port=9000): Max retries exceeded with url: /?properties=%7B%22outputFormat%22%3A+%22json%22%2C+%22annotators%22%3A+%22tokenize%2Cssplit%2Cpos%22%2C+%22ssplit.isOneSentence%22%3A+%22true%22%7D (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f09afea0f10>: Failed to establish a new connection: [Errno 111] Connection refused'))",
            "\nDuring handling of the above exception, another exception occurred:\n",
            "\u001b[0;31mConnectionError\u001b[0m                           Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-1-529f734d23d7>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m()\u001b[0m\n\u001b[1;32m     96\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     97\u001b[0m \u001b[0mtokenize\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"A man entered the dealership.\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 98\u001b[0;31m \u001b[0mdetermine_type\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"A man entered the dealership.\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
            "\u001b[0;32m<ipython-input-1-529f734d23d7>\u001b[0m in \u001b[0;36mdetermine_type\u001b[0;34m(sentence)\u001b[0m\n\u001b[1;32m     29\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     30\u001b[0m \u001b[0;32mdef\u001b[0m \u001b[0mdetermine_type\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0msentence\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 31\u001b[0;31m   \u001b[0;32mreturn\u001b[0m \u001b[0mstpos\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtag\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'What is the airspeed of an unladen swallow ?'\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msplit\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     32\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     33\u001b[0m \u001b[0;32mdef\u001b[0m \u001b[0mdeclare\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mdeclaration\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/nltk/tag/stanford.py\u001b[0m in \u001b[0;36mtag\u001b[0;34m(self, sentence)\u001b[0m\n\u001b[1;32m    229\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    230\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0mtag\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0msentence\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 231\u001b[0;31m         \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtag_sents\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0msentence\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;36m0\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    232\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    233\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0mraw_tag_sents\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0msentences\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/nltk/tag/stanford.py\u001b[0m in \u001b[0;36mtag_sents\u001b[0;34m(self, sentences)\u001b[0m\n\u001b[1;32m    225\u001b[0m         \u001b[0;31m# Converting list(list(str)) -> list(str)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    226\u001b[0m         \u001b[0msentences\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34m(\u001b[0m\u001b[0;34m' '\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mjoin\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mwords\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;32mfor\u001b[0m \u001b[0mwords\u001b[0m \u001b[0;32min\u001b[0m \u001b[0msentences\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 227\u001b[0;31m         \u001b[0;32mreturn\u001b[0m \u001b[0mlist\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mraw_tag_sents\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0msentences\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    228\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    229\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/nltk/tag/stanford.py\u001b[0m in \u001b[0;36mraw_tag_sents\u001b[0;34m(self, sentences)\u001b[0m\n\u001b[1;32m    242\u001b[0m         \u001b[0mdefault_properties\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'annotators'\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m+=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtagtype\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    243\u001b[0m         \u001b[0;32mfor\u001b[0m \u001b[0msentence\u001b[0m \u001b[0;32min\u001b[0m \u001b[0msentences\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 244\u001b[0;31m             \u001b[0mtagged_data\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mapi_call\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0msentence\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mproperties\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mdefault_properties\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    245\u001b[0m             \u001b[0;32massert\u001b[0m \u001b[0mlen\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mtagged_data\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'sentences'\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;34m==\u001b[0m \u001b[0;36m1\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    246\u001b[0m             \u001b[0;31m# Taggers only need to return 1-best sentence.\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/nltk/parse/corenlp.py\u001b[0m in \u001b[0;36mapi_call\u001b[0;34m(self, data, properties)\u001b[0m\n\u001b[1;32m    246\u001b[0m             },\n\u001b[1;32m    247\u001b[0m             \u001b[0mdata\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mdata\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mencode\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mencoding\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 248\u001b[0;31m             \u001b[0mtimeout\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;36m60\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    249\u001b[0m         )\n\u001b[1;32m    250\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/requests/sessions.py\u001b[0m in \u001b[0;36mpost\u001b[0;34m(self, url, data, json, **kwargs)\u001b[0m\n\u001b[1;32m    576\u001b[0m         \"\"\"\n\u001b[1;32m    577\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 578\u001b[0;31m         \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mrequest\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'POST'\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0murl\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mdata\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mdata\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mjson\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mjson\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mkwargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    579\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    580\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0mput\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0murl\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mdata\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;32mNone\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mkwargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/requests/sessions.py\u001b[0m in \u001b[0;36mrequest\u001b[0;34m(self, method, url, params, data, headers, cookies, files, auth, timeout, allow_redirects, proxies, hooks, stream, verify, cert, json)\u001b[0m\n\u001b[1;32m    528\u001b[0m         }\n\u001b[1;32m    529\u001b[0m         \u001b[0msend_kwargs\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mupdate\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0msettings\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 530\u001b[0;31m         \u001b[0mresp\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msend\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mprep\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0msend_kwargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    531\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    532\u001b[0m         \u001b[0;32mreturn\u001b[0m \u001b[0mresp\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/requests/sessions.py\u001b[0m in \u001b[0;36msend\u001b[0;34m(self, request, **kwargs)\u001b[0m\n\u001b[1;32m    641\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    642\u001b[0m         \u001b[0;31m# Send the request\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 643\u001b[0;31m         \u001b[0mr\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0madapter\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msend\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mrequest\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mkwargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    644\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    645\u001b[0m         \u001b[0;31m# Total elapsed time of the request (approximately)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/requests/adapters.py\u001b[0m in \u001b[0;36msend\u001b[0;34m(self, request, stream, timeout, verify, cert, proxies)\u001b[0m\n\u001b[1;32m    514\u001b[0m                 \u001b[0;32mraise\u001b[0m \u001b[0mSSLError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0me\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mrequest\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mrequest\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    515\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 516\u001b[0;31m             \u001b[0;32mraise\u001b[0m \u001b[0mConnectionError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0me\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mrequest\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mrequest\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    517\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    518\u001b[0m         \u001b[0;32mexcept\u001b[0m \u001b[0mClosedPoolError\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0me\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mConnectionError\u001b[0m: HTTPConnectionPool(host='localhost', port=9000): Max retries exceeded with url: /?properties=%7B%22outputFormat%22%3A+%22json%22%2C+%22annotators%22%3A+%22tokenize%2Cssplit%2Cpos%22%2C+%22ssplit.isOneSentence%22%3A+%22true%22%7D (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f09afea0f10>: Failed to establish a new connection: [Errno 111] Connection refused'))"
          ]
        }
      ]
    }
  ]
}