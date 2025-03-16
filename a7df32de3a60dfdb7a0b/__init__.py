import os
import re
import hashlib
import random
import requests
import datetime
from datetime import datetime as datett
from datetime import timedelta, date, timezone
from time import sleep
import pytz
import pandas as pd
import dotenv
import json
import logging
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from typing import AsyncGenerator
import pickle
import zipfile
from exorde_data import (
    Item,
    Content,
    Author,
    CreatedAt,
    Title,
    Url,
    Domain,
    ExternalId,
    ExternalParentId,
)
import subprocess
import shutil
import signal

# import geckodriver_autoinstaller

global driver
global MULTI_ACCOUNT_MODE
global status_rate_limited
global MAX_EXPIRATION_SECONDS
global RATE_LIMITED
global _EMAIL, _USERNAME, _PASSWORD, _COOKIE_FP, _PROXY
global ITEMS_PRODUCED_SESSION
ITEMS_PRODUCED_SESSION = 0
RATE_LIMITED = False
MULTI_ACCOUNT_MODE = False
PROXY_ACCOUNT_MAP_FP = "proxy_account_list.json"
MAX_EXPIRATION_SECONDS = 1800
DEFAULT_ROTATION_DURATION = 3600
special_mode = True
NB_SPECIAL_CHECKS = 6
status_rate_limited = False
# Global variable declaration
_PROXY = None
_EMAIL = None
_USERNAME = None
_PASSWORD = None
_COOKIE_FP = None
driver = None

ONLINE_KW_LIST_URL = "https://raw.githubusercontent.com/exorde-labs/TestnetProtocol/refs/heads/main/targets/keywords.txt"

##### SPECIAL MODE
# TOP 222
SPECIAL_KEYWORDS_LIST = [    
    "the",
    "the",
    "lord",
    "ords",
    "brc20",
    "paris2024",
    "paris2024",
    "olympic",
    "olympic",
    "Acura",
    "Alfa Romeo",
    "Aston Martin",
    "Audi",
    "Bentley",
    "BMW",
    "Buick",
    "Cadillac",
    "Chevrolet",
    "Chrysler",
    "Dodge",
    "Ferrari",
    "Fiat",
    "Ford",
    "Genesis",
    "GMC",
    "Honda",
    "Hyundai",
    "Infiniti",
    "Jaguar",
    "Jeep",
    "Kia",
    "Lamborghini",
    "Land Rover",
    "Lexus",
    "Lincoln",
    "Lotus",
    "Maserati",
    "Mazda",
    "Taiko",
    "Taiko labs",
    "McLaren",
    "Mercedes-Benz",
    "MINI",
    "Mitsubishi",
    "Nissan",
    "Porsche",
    "Ram",
    "Renault",
    "Rolls-Royce",
    "Subaru",
    "Tesla",
    "Toyota",
    "Volkswagen",
    "Volvo",    
    "BlackRock",
    "Vanguard",
    "State Street",
    "advisors",
    "Fidelity",
    "Fidelity Investments",
    "Asset Management",
    "Asset",
    "digital asset",
    "NASDAQ Composite",
    "Dow Jones Industrial Average",
    "Gold",
    "Silver",
    "Brent Crude",
    "WTI Crude",
    "EUR",
    "US",
    "YEN"
    "UBS",
    "PIMCO",
    "schroders",
    "aberdeen",    
    "louis vuitton",
    "moet Chandon",
    "hennessy",
    "dior",
    "fendi",
    "givenchy",
    "celine",
    "tag heuer",
    "bvlgari",
    "dom perignon",
    "hublot",
    "Zenith",    
    "meme", 
    "coin", 
    "memecoin", 
    "pepe", 
    "doge", 
    "shib",
    "floki",
    "dogtoken",
    "trump token",
    "barron token",    
    "DOGE",
    "SHIB",
    "PEPE",
    "BONK",
    "WIF",
    "FLOKI",
    "MEME",    
    "DOGE",
    "SHIB",
    "PEPE",
    "BONK",
    "WIF",
    "FLOKI",
    "MEME",
    "DOGE",
    "SHIB",
    "PEPE",
    "BONK",
    "WIF",
    "FLOKI",
    "MEME",
    "TRUMP",
    "BabyDoge",
    "ERC20",
    "BONE",
    "COQ",
    "WEN",
    "BITCOIN",
    "ELON",
    "SNEK",
    "MYRO",
    "PORK",
    "TOSHI",
    "SMOG",
    "LADYS",
    "AIDOGE",
    "TURBO",
    "TOKEN",
    "SAMO",
    "KISHU",
    "TSUKA",
    "LEASH",
    "QUACK",
    "VOLT",
    "PEPE2.0",
    "JESUS",
    "MONA",
    "DC",
    "WSM",
    "PIT",
    "QOM",
    "PONKE",
    "SMURFCAT",
    "AKITA",
    "VINU",
    "ANALOS",
    "BAD",
    "CUMMIES",
    "HONK",
    "HOGE",
    "$MONG",
    "SHI",
    "BAN",
    "RAIN",
    "TAMA",
    "PAW",
    "SPX",
    "HOSKY",
    "BOZO",
    "DOBO",
    "PIKA",
    "CCC",
    "REKT",
    "WOOF",
    "MINU",
    "WOW",
    "PUSSY",
    "KEKE",
    "DOGGY",
    "KINGSHIB",
    "CHEEMS",
    "SMI",
    "OGGY",
    "DINGO",
    "DONS",
    "GRLC",
    "AIBB",
    "CATMAN",
    "XRP",
    "CAT",
    "数字資産",  # Digital Asset (Japanese)
    "仮想",  # Virtual (Japanese)
    "仮想通貨",  # Virtual Currency (Japanese)
    "自動化",  # Automation (Japanese)
    "アルゴリズム",  # Algorithm (Japanese)
    "コード",  # Code (Japanese)
    "機械学習",  # Machine Learning (Japanese)
    "ブロックチェーン",  # Blockchain (Japanese)
    "サイバーセキュリティ",  # Cybersecurity (Japanese)
    "人工",  # Artificial (Japanese)
    "合成",  # Synthetic (Japanese)
    "主要",  # Major (Japanese)
    "IoT",
    "クラウド",  # Cloud (Japanese)
    "ソフトウェア",  # Software (Japanese)
    "API",
    "暗号化",  # Encryption (Japanese)
    "量子",  # Quantum (Japanese)
    "ニューラルネットワーク",  # Neural Network (Japanese)
    "オープンソース",  # Open Source (Japanese)
    "ロボティクス",  # Robotics (Japanese)
    "デブオプス",  # DevOps (Japanese)
    "5G",
    "仮想現実",  # Virtual Reality (Japanese)
    "拡張現実",  # Augmented Reality (Japanese)
    "バイオインフォマティクス",  # Bioinformatics (Japanese)
    "ビッグデータ",  # Big Data (Japanese)
    "大統領",  # President (Japanese)
    "行政",  # Administration (Japanese)
    "Binance",
    "Bitcoin ETF",
    "政治",  # Politics (Japanese)
    "政治的",  # Political (Japanese)
    "ダイアグラム",  # Diagram (Japanese)
    "$algo",
    "$algo",
    "%23CAC",
    "%23G20",
    "%23IPO",
    "%23NASDAQ",
    "%23NYSE",
    "%23OilPrice",
    "%23SP500",
    "%23USD",
    "%23airdrop",
    "%23altcoin",
    "%23bonds",
    "%23price",
    "AI",
    "AI",
    "AI",
    "AI",
    "AUDNZD",
    "Alphabet%20(GOOG)",
    "Apple",
    "Aprendizaje Automático",
    "BNB",
    "Berkshire",
    "Biden administration",
    "Binance",
    "Bitcoin%20ETF",
    "Black%20Rock",
    "BlackRock",
    "BlackRock",
    "Branche",
    "Brazil",
    "CAC40",
    "COIN",
    "Canada",
    "China",
    "Coinbase",
    "Congress",
    "Crypto",
    "Crypto",
    "Crypto",
    "Cryptocurrencies",
    "Cryptos",
    "DeFi",
    "Diagramm",
    "Dios mío",
    "DowJones",
    "ETF",
    "ETFs",
    "EU",
    "EU",
    "EURUSD",
    "Elon",
    "Elon",
    "Elon",
    "Elon%20musk",
    "Europe",
    "European%20union%20(EU)",
    "FB%20stock",
    "FTSE",
    "Firma",
    "France",
    "GDP",
    "GPU",
    "GameFi",
    "Gensler",
    "Germany",
    "Gerücht",
    "Geschäft",
    "Gesundheit",
    "Gewinn",
    "Gewinn",
    "Heilung",
    "IA",
    "IA",
    "IPO",
    "Israel",
    "Israel",
    "Israel",
    "Juego",
    "KI",
    "Konflikt",
    "Kraken",
    "LGBTQ rights",
    "LVMH",
    "Land",
    "Luxus",
    "Marke",
    "Maschinelles Lernen",
    "Mexico",
    "NFLX",
    "NFT",
    "NFT",
    "NFTs",
    "NYSE",
    "Nachrichten",
    "Nasdaq%20100",
    "Oh Dios mío",
    "Openfabric",
    "Openfabric AI",
    "Openfabric",
    "OFN",
    "PLTR",
    "Palestine",
    "Palestine",
    "Palestine",
    "País",
    "Politik",
    "Produkt",
    "Roe v. Wade",
    "Silicon Valley",
    "Spiel",
    "Spot%20ETF",
    "Start-up",
    "Streaming",
    "Supreme Court",
    "Technologie",
    "Tesla",
    "UE",
    "UE",
    "USA",
    "USDEUR",
    "United%20states",
    "Unterhaltung",
    "Verlust",
    "Virus",
    "Vorhersage",
    "WallStreet",
    "WarrenBuffett",
    "Warren Buffett",
    "Web3",
    "X.com",
    "XAUUSD",
    "Xitter",
    "abortion",
    "achetez",
    "actualité",
    "airdrop",
    "airdrops",
    "alert",
    "algorand",
    "algorand",
    "algorand",
    "amazon",
    "analytics",
    "announcement",
    "apprentissage",
    "artificial intelligence",
    "artificial intelligence",
    "asset",
    "asset%20management",
    "attack",
    "attack",
    "attack",
    "attentat",
    "authocraty",
    "balance sheet",
    "bank",
    "bear",
    "bearish",
    "bears",
    "beliebt",
    "bezos",
    "biden",
    "biden",
    "biden",
    "biden",
    "data",
    "develop",
    "virtual",
    "automation",
    "algorithm",
    "code",
    "machine learning",
    "blockchain",
    "cybersecurity",
    "artificial",
    "synth",
    "synthetic",
    "major",
    "IoT",
    "cloud",
    "software",
    "API",
    "encryption",
    "quantum",
    "neural",
    "open source",
    "robotics",
    "devop",
    "5G",
    "virtual reality",
    "augmented reality",
    "bioinformatics",
    "big data",
    "billion",
    "bitcoin",
    "bizness",
    "blockchain",
    "bond",
    "breaking news",
    "breaking%20news",
    "btc",
    "btc",
    "btc",
    "btc",
    "btc",
    "btc",
    "btc",
    "btc",
    "budget",
    "bull",
    "bullish",
    "bulls",
    "business",
    "businesses",
    "buy support",
    "cardano",
    "cash flow",
    "cbdc",
    "choquant",
    "climate change action",
    "climate change",
    "climate tech startups",
    "communist",
    "companies",
    "company",
    "compound interest",
    "compra ahora"
    "compra",
    "conflict",
    "conflict",
    "conflicto",
    "conflit",
    "congress",
    "conservatives",
    "corporate",
    "corporation",
    "credit",
    "crime",
    "crisis",
    "crude%20oil",
    "crypto",
    "crypto",
    "crypto",
    "crypto",
    "crypto",
    "cryptocurrency",
    "cryptocurrency",
    "cura",
    "currencies",
    "currency",
    "currency",
    "database",
    "debit",
    "debt",
    "debt",
    "decentralized finance",
    "decentralized",
    "decline",
    "deep learning",
    "defi",
    "democracy",
    "diffusion",
    "digital",
    "divertissement",
    "dividend",
    "doge",
    "dogecoin",
    "démarrage",
    "e-commerce",
    "economy",
    "economy",
    "education startups",
    "education",
    "elections",
    "elisee",
    "embargo",
    "embassy",
    "empresa",
    "entreprise",
    "entretenimiento",
    "equity",
    "erc20",
    "eth",
    "eth",
    "eth",
    "eth",
    "eth",
    "ethereum",
    "exchange rate",
    "expense",
    "extremism",
    "fair%20launch",
    "fascist",
    "finance",
    "finance",
    "financial advisor",
    "financial planning",
    "financing",
    "fintech",
    "fintech",
    "fintech",
    "fiscal policy",
    "fixed income",
    "foreign aid",
    "foreign exchange",
    "foreign policy",
    "forex",
    "forex",
    "founder CEO",
    "founders",
    "fusion",
    "gagner",
    "gain",
    "ganancia",
    "ganar",
    "gas",
    "gaza",
    "gaza",
    "gaza",
    "government",
    "governments",
    "graphique",
    "gross domestic product",
    "growth",
    "gráfico",
    "gun control",
    "gun violence prevention",
    "hamas",
    "hamas",
    "hamas",
    "hamas",
    "healthcare startups",
    "healthcare",
    "helion",
    "hft trading",
    "holdings",
    "hostage",
    "hostage",
    "immigration reform",
    "immigration",
    "impactante",
    "impactante",
    "impeachment",
    "income",
    "increíble",
    "increíble",
    "incroyable",
    "industria",
    "industrie",
    "inflation",
    "inflation",
    "infrastructure",
    "insider trading",
    "insider",
    "insurance",
    "intraday",
    "investing",
    "investment",
    "investor",
    "investors",
    "jerusalem",
    "jeu",
    "kaufen",
    "kremlin",
    "legal",
    "legal%20tender",
    "liability",
    "libertarian",
    "liquidity",
    "loan",
    "long",
    "lujo",
    "luxe",
    "machine learning",
    "macron",
    "macron",
    "macron",
    "en marche",
    "parti",
    "marca",
    "margin",
    "mark%20zuckerberg",
    "market capitalization",
    "market maker",
    "market",
    "markets",
    "marque",
    "mein Gott",
    "middle east",
    "middle east",
    "middle east",
    "million",
    "mint",
    "missile",
    "missile",
    "missile",
    "mon Dieu",
    "monero",
    "money",
    "mortgage",
    "moscow",
    "mutual fund",
    "nasdaq",
    "national security",
    "national%20emergency",
    "national%20security",
    "natural%20gas",
    "negocios",
    "net income",
    "net worth",
    "new project",
    "new startup",
    "news",
    "newsfeed",
    "newsflash",
    "nft",
    "nft%20latform",
    "nftcommunity",
    "nfts",
    "noticias",
    "nuclear",
    "official",
    "oil",
    "parliament",
    "pays",
    "perder",
    "perdido",
    "perdre",
    "perdu",
    "plummet",
    "police",
    "politician",
    "politicians",
    "politique",
    "polkadot",
    "polygon",
    "política",
    "populaire",
    "popular",
    "populism",
    "portfolio",
    "predicción",
    "press",
    "price-to-earnings ratio",
    "producto",
    "produit",
    "profit",
    "promising company",
    "protocols",
    "prédiction",
    "putin",
    "putin",
    "putin",
    "putin",
    "poutine",
    "poutine",
    "poutine",
    "poutine",
    "vladimir putin",
    "vladimir putin",
    "vladimir putin",
    "xi jinping",
    "xi jinping",
    "xi jinping",
    "racial justice",
    "recession",
    "renault trucks",
    "renault trucks",
    "renault",
    "renault",
    "resistance sell",
    "retirement planning",
    "return on investment",
    "riots",
    "ripple",
    "risk",
    "robotics",
    "rumeur",
    "rumor",
    "russia",
    "s&p500",
    "sales",
    "salud",
    "sam20altman",
    "santé",
    "satoshi",
    "schockierend",
    "scraping",
    "securities",
    "security%20token",
    "self-driving cars",
    "senate",
    "senator",
    "senators",
    "shardeum",
    "short",
    "silvio micali",
    "solana",
    "solana%20sol",
    "sp500",
    "space exploration",
    "space tech startups",
    "stablecoin",
    "startup",
    "startup",
    "stock market",
    "stock",
    "stocks",
    "streaming",
    "syria",
    "takeoff",
    "tax",
    "tech startups",
    "technologie",
    "technology",
    "tecnología",
    "token",
    "toyota",
    "trade",
    "trading",
    "trading",
    "traitement",
    "treasury bill",
    "trump",
    "trump",
    "trump",
    "trump",
    "vote",
    "vote",
    "vote",
    "election",
    "election",
    "election",
    "voter",
    "voter",
    "million",
    "club",
    "tech",
    "nvda",
    "machine",
    "generative",
    "reinforcement",
    "official",
    "twitter",
    "ukraine",
    "unglaublich",
    "unicorns",
    "unicorns",
    "us%20president",
    "usdt",
    "usdt",
    "usdt",
    "usdt",
    "utility%20token",
    "venture capital",
    "venture capital",
    "venture capital",
    "verloren",
    "virus",
    "virus",
    "volvo group",
    "volvo trucks",
    "volvo",
    "voting rights",
    "wall street",
    "war in Ukraine",
    "war",
    "web3",
    "web3",
    "white house",
    "worldcoin",
    "xrp",
    "yield",
    "zero knowledge",
    "zksync",    
    "renewables",
    "energy",
    "infrastructure",
    "infrastructure investment",
    "FDI investment",
    "foreign investment",
    "foreign policy",
    "new policy",
    "new policies",
    "ГПУ",
    "ЕС",
    "ИИ",
    "Игра",
    "Илон",
    "Машинное обучение",
    "Страна",
    "бизнес",
    "бренд",
    "вирус",
    "график",
    "здоровье",
    "индустрия",
    "компания",
    "конфликт",
    "купи сейчас",
    "лечение",
    "невероятный",
    "новости",
    "о боже мой",
    "победа",
    "политика",
    "популярный",
    "поражение",
    "потеря",
    "потоковая передача",
    "прибыль",
    "прогноз",
    "продукт",
    "развлечение",
    "роскошь",
    "слух",
    "стартап",
    "технологии",
    "шокирующий",
    "أخبار",
    "أعمال",
    "إيلون",
    "اشتر الآن",
    "الاتحاد الأوروبي",
    "الذكاء الاصطناعي",
    "بث مباشر",
    "بلد",
    "ترفيه",
    "تعلم الآلة",
    "تكنولوجيا",
    "توقع",
    "خسارة",
    "رائع",
    "ربح",
    "رسم بياني",
    "سياسة",
    "شائعة",
    "شركة ناشئة",
    "شركة",
    "شهير",
    "صادم",
    "صحة",
    "صراع",
    "صناعة",
    "ضائع",
    "علاج",
    "علامة تجارية",
    "فخامة",
    "فوز",
    "فيروس",
    "لعبة",
    "منتج",
    "وحدة معالجة الرسومات",
    "يا إلهي",
    "ああ、神様",
    "イーロン",
    "ウイルス",
    "エンターテインメント",
    "ゲーム",
    "スタートアップ",
    "ストリーミング",
    "チャート",
    "テクノロジー",
    "ニュース",
    "ビジネス",
    "ブランド",
    "业务",
    "予測",
    "产品",
    "人工智能",
    "人気",
    "今買う",
    "令人难以置信",
    "令人震惊",
    "会社",
    "信じられない",
    "健康",
    "健康",
    "公司",
    "冲突",
    "初创企业",
    "利益",
    "勝利",
    "品牌",
    "哦，我的天啊",
    "噂",
    "国",
    "国家",
    "图表",
    "埃隆",
    "失われた",
    "失去",
    "娱乐",
    "技术",
    "收益",
    "政治",
    "政治",
    "敗北",
    "新闻",
    "机器学习",
    "機械学習",
    "欧盟",
    "治疗",
    "治療",
    "流媒体",
    "游戏",
    "热门",
    "産業",
    "病毒",
    "立刻购买",
    "紛争",
    "行业",
    "衝撃的",
    "製品",
    "谣言",
    "豪华",
    "赢",
    "输",
    "预测",
    "高級",
    'the', 'of', 'and', 'a', 'in', 'to', 'is', 'that', 'it', 'for', 'on', 'you', 'this', 'with', 'as', 'I', 'be', 'at', 'by', 'from', 
    'or', 'an', 'have', 'not', 'are', 'but', 'we', 'they', 'which', 'one', 'all', 'their', 'there', 'can', 'has', 'more', 'do', 'if', 
    'will', 'about', 'up', 'out', 'who', 'get', 'like', 'when', 'just', 'my', 'your', 'what',
    'el', 'de', 'y', 'a', 'en', 'que', 'es', 'la', 'lo', 'un', 'se', 'no', 'con', 'una', 'por', 'para', 'está', 'son', 'me', 'si', 
    'su', 'al', 'desde', 'como', 'todo', 'está',
    '的', '是', '了', '在', '有', '和', '我', '他', '这', '就', '不', '要', '会', '能', '也', '去', '说', '所以', '可以', '一个',
    'का', 'है', 'हों', 'पर', 'ने', 'से', 'कि', 'यह', 'तक', 'जो', 'और', 'एक', 'हिंदी', 'नहीं', 'आप', 'सब', 'तो', 'मुझे', 'इस', 'को',
    'في', 'من', 'إلى', 'على', 'مع', 'هو', 'هي', 'هذا', 'تلك', 'ون', 'كان', 'لك', 'عن', 'ما', 'ليس', 'كل', 'لكن', 'أي', 'ودي', 'أين',
    'র', 'এ', 'আমি', 'যা', 'তা', 'হয়', 'হবে', 'তুমি', 'কে', 'তার', 'এখন', 'এই', 'কিন্তু', 'মাঠ', 'কি', 'আপনি', 'বাহী', 'মনে', 'তাহলে', 'কেন', 'থাক',
    'o', 'a', 'e', 'de', 'do', 'da', 'que', 'não', 'em', 'para', 'como', 'com', 'um', 'uma', 'meu', 'sua', 'se', 'este', 'esse', 'isto',
    'в', 'и', 'не', 'на', 'что', 'как', 'что', 'он', 'она', 'это', 'но', 'с', 'из', 'по', 'к', 'то', 'да', 'был', 'который', 'кто',
    'の', 'に', 'は', 'を', 'です', 'ます', 'た', 'て', 'いる', 'い', 'この', 'それ', 'あ', '等', 'や', 'も', 'もし', 'いつ', 'よ', 'お',
    'der', 'die', 'das', 'und', 'in', 'zu', 'von', 'mit', 'ist', 'an', 'bei', 'ein', 'eine', 'nicht', 'als', 'auch', 'so', 'wie', 'was', 'oder',
    'le', 'la', 'à', 'de', 'et', 'un', 'une', 'dans', 'ce', 'que', 'il', 'elle', 'est', 's', 'des', 'pour', 'par', 'au', 'en', 'si',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    ' truth', 'abortion', 'academics', 'accessible tourism', 'accountability', 'acquiring companies', 'active funds', 'active learning', 'actorcritic methods', 'adaptive investing',
    'adaptive learning', 'addiction', 'ads cft', 'adventure tourism', 'advertorials', 'advisors', 'affiliate marketing', 'affirmative action', 'affordable housing', 'affordable luxury',
    'afforestation', 'afghan war', 'afghanistan war', 'agenda ', 'agile investing', 'agile work', 'agritourism', 'ai', 'ai alignment', 'aid for trade',
    'aids', 'algeria protests', 'algos', 'alloys', 'aluminium', 'aluminum', 'ambush marketing', 'analysts', 'analytics', 'anarchism',
    'anthropic principle', 'antimony', 'antisemitism', 'antitrust', 'antivaccination', 'antivax', 'apprenticeships', 'arab spring', 'arbitrageurs', 'arctic geopolitics',
    'area ', 'arms control', 'arms race', 'arms trafficking', 'art market', 'aspirational brands', 'assassinations', 'assayers', 'asset allocation', 'asteroid mining',
    'astrobiology', 'astrotourism', 'asylum', 'asymmetric warfare', 'asynchronous work', 'atrocity prevention', 'augmented reality', 'authoritarianism', 'automation', 'autonomous vehicles',
    'autonomous weapons', 'averages', 'b corps', 'balanced investing', 'banking', 'bankrupt companies', 'banks', 'banner ads', 'bars', 'base metals',
    'beacons', 'bears', 'behavioral cloning', 'belarus protests', 'bells theorem', 'benchmarks', 'beneficial ai', 'bequests', 'beryllium', 'bespoke',
    'beyond gdp', 'bid rigging', 'big bang', 'big data', 'big tech', 'bike lanes', 'bike sharing', 'bilateral alliances', 'bilateral diplomacy', 'biodiversity loss',
    'bioenergy', 'bioengineering', 'birth tourism', 'bismuth', 'bitcoin', 'black holes', 'black lives matter', 'bleisure', 'blended learning', 'blockchain',
    'blood diamonds', 'blue economy', 'bluechip companies', 'bolivia protests', 'bonds', 'border security', 'border wall', 'boxing', 'brainwashing', 'brand integrations',
    'branded content', 'brexit', 'bribery', 'brics', 'brokers', 'budget', 'bullion', 'bulls', 'cadmium', 'cameroon conflict',
    'campaign finance', 'cancel culture', 'cannabis tourism', 'cap and trade', 'capacity building', 'capitalism', 'capitol riot', 'car sharing', 'carbon nanotubes', 'carbon offsetting',
    'carbon pricing', 'carbon tax', 'carfree cities', 'carpooling', 'carveout companies', 'cause marketing', 'celebrity diplomacy', 'censorship', 'cerium', 'cern',
    'certification', 'chain alliances', 'character education', 'charities', 'chartists', 'chatbots', 'chemicals', 'chemtrails', 'child health', 'child labor',
    'chile protests', 'chromium', 'circular economy', 'circular investing', 'circular marketing', 'citizens dividend', 'citizens united', 'citizenship', 'city branding', 'city diplomacy',
    'civil liberties', 'civil rights', 'civil unrest', 'climate action', 'climate adaptation', 'climate diplomacy', 'climate finance', 'climate justice', 'climate mitigation', 'closed alliances',
    'closedend funds', 'cluster alliances', 'cobalt', 'cobranding', 'coins', 'cold calling', 'coliving', 'collective memory', 'collectors', 'college',
    'colombia protests', 'color revolutions', 'commentators', 'commerce', 'commercials', 'communism', 'competition policy', 'concentrates', 'conflict minerals', 'conflict prevention',
    'conflict resolution', 'conglomerates', 'congress', 'conscious investing', 'conservatism', 'conspiracy theories', 'consultants', 'consumer protection', 'content marketing', 'continual learning',
    'contraception', 'contrarians', 'cooperatives', 'copper', 'copyleft', 'copyright', 'coral bleaching', 'coronavirus', 'correlation', 'corrigibility',
    'corruption', 'cosmetics', 'cosmic rays', 'cottage industries', 'counterfeit goods', 'counterinsurgency', 'counterintelligence', 'counterterrorism', 'coup detat', 'covert alliances',
    'covert operations', 'covid', 'coworking', 'creative commons', 'creative economy', 'creator economy', 'credit unions', 'crimea annexation', 'criminal justice', 'crisis actors',
    'crisis management', 'crisis response', 'critical metals', 'crosspromotion', 'crowdfunding', 'cryonics', 'crypto art', 'cryptocurrency', 'culinary tourism', 'cultural diplomacy',
    'cultural heritage', 'cultural property', 'cultural tourism', 'curfew', 'cyberattacks', 'cybercrime', 'cybersecurity', 'cyberwarfare', 'cycles', 'cyclical companies',
    'd bioprinting', 'd printing', 'dark ages', 'dark energy', 'dark matter', 'dark money', 'dark tourism', 'data breaches', 'data protection', 'dealers',
    'death penalty', 'death tourism', 'debate', 'debt', 'decarbonization', 'declining companies', 'deep learning', 'deep state', 'defense', 'defense policy',
    'defensive alliances', 'defensive companies', 'defensive investing', 'deficit', 'deforestation', 'degrowth', 'dental tourism', 'deportation', 'deradicalization', 'deregulation',
    'desertification', 'developers', 'diaspora diplomacy', 'dictatorship', 'digital diplomacy', 'digital divide', 'digital nomad', 'digital nomads', 'diplomacy', 'direct selling',
    'disability rights', 'discrimination', 'disinformation', 'distance education', 'distributed energy', 'diversification', 'diversity marketing', 'divesting companies', 'dividend companies', 'domestic alliances',
    'domestic companies', 'domestic violence', 'donations', 'donbas war', 'donoradvised funds', 'doomsayers', 'doortodoor selling', 'doughnut economics', 'dr congo conflict', 'drake equation',
    'dreamers', 'drm', 'drone warfare', 'drones', 'drought', 'drug policy reform', 'drug safety', 'drug trafficking', 'dust', 'dynamic alliances',
    'dynamic investing', 'dysprosium', 'early warning', 'ecoentrepreneurship', 'ecommerce', 'economic sanctions', 'economists', 'economy', 'ecosystem alliances', 'ecotourism',
    'education', 'educational tourism', 'elearning', 'elections', 'electoral college', 'electric vehicles', 'email marketing', 'embezzlement', 'emerging markets', 'emissions trading',
    'emotional marketing', 'employee ownership', 'encryption', 'endangered species', 'endorsements', 'endowments', 'energy diplomacy', 'energy efficiency', 'energy justice', 'energy storage',
    'energy transition', 'engineers', 'enhanced weathering', 'enthusiasts', 'entrepreneurship', 'equity alliances', 'erbium', 'esg investing', 'espionage', 'espionage act',
    'esports', 'estates', 'estimates', 'etfs', 'ethereum', 'ethical investing', 'ethical tourism', 'ethical trade', 'ethics', 'ethiopia conflict',
    'ethnic cleansing', 'european union', 'europium', 'event marketing', 'exclusive alliances', 'existential risk', 'experts', 'explainable ai', 'explicit alliances', 'explorers',
    'export credits', 'export marketing', 'extradition', 'extremism', 'fabricators', 'factored cognition', 'factories', 'failed states', 'fair trade', 'fair use',
    'fairness', 'fake news', 'false flag', 'family offices', 'family planning', 'famine', 'fascism', 'federal reserve', 'fellowships', 'fema camps',
    'feminism', 'fermi paradox', 'ferrous metals', 'fertility tourism', 'fewshot learning', 'fine tuned universe', 'first amendment', 'first stars', 'fiscal policy', 'fish trafficking',
    'fisheries crime', 'flat earth', 'fleet management', 'flexible investing', 'flexible work', 'flexitarian', 'flipped classroom', 'flying cars', 'food deserts', 'food diplomacy',
    'food justice', 'food safety', 'food waste', 'forced labor', 'forecasts', 'foreign affairs', 'foreign aid', 'foreign companies', 'foreign policy', 'forest crime',
    'formal alliances', 'forward integration', 'foundations', 'foundries', 'fourday workweek', 'fragile states', 'franchising', 'fraud', 'free speech', 'freelancing',
    'friendly ai', 'frozen conflicts', 'fuel cells', 'fullerenes', 'fundamentalists', 'fusion power', 'future generations', 'futures', 'g', 'gadolinium',
    'galaxy formation', 'gallium', 'gamefi', 'gamification', 'gamma ray bursts', 'gastrodiplomacy', 'gay marriage', 'gcc crisis', 'gdpr', 'gender equality',
    'gene editing', 'genocide', 'genocide prevention', 'genomic medicine', 'gentrification', 'geoengineering', 'geofencing', 'geologists', 'geopolitics', 'georgia conflict',
    'geothermal', 'geothermal energy', 'geotourism', 'germanium', 'gerrymandering', 'gifts', 'gig economy', 'gini coefficient', 'girls education', 'global alliances',
    'global companies', 'globalism', 'globalization', 'glocal marketing', 'gmo', 'gold', 'government', 'grants', 'graphene', 'gravitational waves',
    'green bonds', 'green buildings', 'green card', 'green economy', 'green finance', 'green investing', 'green logistics', 'green marketing', 'green new deal', 'grey goo',
    'growth companies', 'growth investing', 'guerrilla marketing', 'gun control', 'gurus', 'hacking', 'hafnium', 'haiti protests', 'halal tourism', 'handmade',
    'harm reduction', 'hate crimes', 'hate speech', 'hazardous waste', 'healthcare', 'hedgers', 'hedging', 'heritage tourism', 'higgs boson', 'highrisk investing',
    'highspeed rail', 'historical memory', 'hiv', 'hoarders', 'hobbyists', 'holding companies', 'holmium', 'holocaust', 'holocaust education', 'homelessness',
    'hong kong protests', 'hubble constant', 'human compatible ai', 'human enhancement', 'human rights', 'human trafficking', 'hybrid warfare', 'hybrid work', 'hydroelectric', 'hydrogen',
    'hydrogen fuel cells', 'hydropower', 'hyperloop', 'hypersonic weapons', 'identity politics', 'identity theft', 'illegal fishing', 'illegal logging', 'illegal mining', 'illicit trade',
    'illuminati', 'imf', 'imitation learning', 'immersive marketing', 'immigration', 'impact investing', 'impact measures', 'impactful investing', 'impeachment', 'impeachment trial',
    'implicit alliances', 'inbound marketing', 'inclusive alliances', 'inclusive education', 'inclusive growth', 'inclusive marketing', 'income inequality', 'income investing', 'index funds', 'indicators',
    'indices', 'indigenous rights', 'indium', 'industrial parks', 'industry ', 'inflation', 'infomercials', 'informal alliances', 'information warfare', 'ingame purchases',
    'ingots', 'inheritances', 'innovation hubs', 'insider trading', 'insights', 'insourcing', 'insurance', 'insurance companies', 'integral alliances', 'intelligence',
    'interest rates', 'internet freedom', 'internet of things', 'internships', 'interpretability', 'interruptibility', 'interstellar travel', 'invasive species', 'investigation', 'investing',
    'investors', 'iran nuclear deal', 'iran protests', 'iransaudi rivalry', 'iraq protests', 'iraq war', 'iridium', 'islamophobia', 'isolationism', 'israel',
    'iter', 'january th', 'jewelers', 'jfk assassination', 'job guarantee', 'jobs', 'joint ventures', 'journalism', 'junior miners', 'kashmir conflict',
    'killer robots', 'kosher tourism', 'lab grown meat', 'labeling', 'labor', 'labor rights', 'land degradation', 'land rights', 'lanthanum', 'largecap companies',
    'last mile delivery', 'lateral integration', 'laws', 'lead', 'leaks', 'leave no one behind', 'lebanon protests', 'legacy investing', 'leveraged investing', 'lgbt rights',
    'lgbt tourism', 'lgbtq rights', 'liberalism', 'libertarianism', 'libya conflict', 'libya intervention', 'licensing', 'lifelong learning', 'lifestyle brands', 'lithium',
    'lithium batteries', 'livable cities', 'live commerce', 'living wage', 'lobbying', 'local alliances', 'local companies', 'local marketing', 'local production', 'locavore',
    'logistics', 'longonly investing', 'longshort investing', 'longterm alliances', 'longterm future', 'looted art', 'looting', 'loselose alliances', 'lowcarbon economy', 'lowrisk investing',
    'lutetium', 'luxury', 'machine learning', 'maglev', 'magnesium', 'majorana fermions', 'maker movement', 'malaria', 'mali conflict', 'malnutrition',
    'mandela effect', 'manganese', 'manufacturing', 'market manipulation', 'markets', 'mars colonization', 'martial law', 'mass atrocities', 'mass customization', 'mass extinction',
    'mass shootings', 'mass surveillance', 'masstige', 'maternal health', 'mature companies', 'media', 'mediation', 'medicaid', 'medical devices', 'medical tourism',
    'medicare', 'memorialization', 'mental health', 'mentorships', 'mercury', 'merging companies', 'mesa optimization', 'mesh alliances', 'metalearning', 'metallurgists',
    'metaverse commerce', 'metoo', 'metrics', 'microcap companies', 'microfinance', 'microgrids', 'midcap companies', 'middle east', 'migration', 'mild optimization',
    'military', 'military coup', 'military strategy', 'mind control', 'mind uploading', 'mindful investing', 'minimum wage', 'mining stocks', 'minor metals', 'minority rights',
    'mints', 'misinformation', 'moderate investing', 'modern slavery', 'modular alliances', 'moldova conflict', 'molybdenum', 'momentum companies', 'momentum investing', 'monetary policy',
    'money laundering', 'moon landing hoax', 'mozambique conflict', 'mtheory', 'mueller report', 'multilateralism', 'multitask learning', 'multiverse', 'mutual funds', 'myanmar coup',
    'nanocap companies', 'nanodiamonds', 'nanomedicine', 'nanorobotics', 'nanotechnology', 'nation branding', 'nation building', 'national guard', 'national security', 'nationalism',
    'native ads', 'native advertising', 'nato', 'nazism', 'nearshoring', 'negative income tax', 'negotiation', 'neodymium', 'net metering', 'net neutrality',
    'network alliances', 'network marketing', 'neural engineering', 'neural networks', 'neuromarketing', 'neutrinos', 'neutron stars', 'new world order', 'nickel', 'nigeria conflict',
    'nimble investing', 'nimby', 'niobium', 'noble metals', 'nonequity alliances', 'nonferrous metals', 'nonprofits', 'nonstate actors', 'nord stream ', 'north korea',
    'notforprofits', 'nuclear arms race', 'nuclear energy', 'nuclear safety', 'nuggets', 'obamacare', 'obesity epidemic', 'occupational safety', 'occupy movement', 'ocean acidification',
    'offensive alliances', 'offensive investing', 'official secrets', 'offshore accounts', 'offshore companies', 'offshoring', 'online education', 'onshore companies', 'open alliances', 'open source',
    'openend funds', 'opioid crisis', 'optimists', 'options', 'orange economy', 'ores', 'organic farming', 'organized crime', 'osmium', 'outsourcing',
    'overdose', 'oversight', 'overt alliances', 'palestine', 'palladium', 'palma ratio', 'panama papers', 'pandemic', 'panspermia', 'paradiplomacy',
    'paradise papers', 'parallel universes', 'parasitic alliances', 'paris agreement', 'partnerships', 'passive funds', 'passive house', 'patents', 'patterns', 'peace',
    'peace education', 'peacebuilding', 'peacekeeping', 'peacemaking', 'peertopeer lending', 'pension funds', 'permaculture', 'permanent alliances', 'peru protests', 'pessimists',
    'pesticides', 'pgms', 'phishing', 'pilgrimage', 'pilot wave theory', 'pink tourism', 'pizzagate', 'place branding', 'plastic pollution', 'platform alliances',
    'platform economy', 'platinum', 'playtoearn', 'poaching', 'police brutality', 'policy gradients', 'politics', 'ponzi schemes', 'populism', 'popup ads',
    'posthumanism', 'postscarcity', 'poverty', 'poverty tourism', 'praseodymium', 'precious metals', 'precision medicine', 'predictions', 'premiumization', 'preppers',
    'prescription drugs', 'president', 'press freedom', 'price fixing', 'prison reform', 'privacy', 'privacy laws', 'private alliances', 'private foundations', 'private labeling',
    'proactive alliances', 'proactive investing', 'producers', 'product placement', 'product placements', 'product safety', 'professors', 'profit sharing', 'progressivism', 'projections',
    'promethium', 'propaganda', 'propoor growth', 'protectionism', 'protests', 'provenance research', 'proximity marketing', 'proxy wars', 'psychedelic tourism', 'psychedelics',
    'public alliances', 'public diplomacy', 'public domain', 'public health', 'public transport', 'pulsars', 'pundits', 'purple economy', 'push notifications', 'pyramid schemes',
    'qanon', 'qatar blockade', 'quality companies', 'quality education', 'quants', 'quantum biology', 'quantum cognition', 'quantum computing', 'quantum gravity', 'quantum supremacy',
    'quasars', 'racial justice', 'radicalism', 'radicalization', 'rainbow tourism', 'rankings', 'ransomware', 'rapid prototyping', 'rare earths', 'ratings',
    'ratios', 'reactive alliances', 'realists', 'rebalancing', 'recession', 'reconciliation', 'recyclers', 'ree', 'referral marketing', 'referrals',
    'refiners', 'reforestation', 'refugee crisis', 'refugees', 'regime change', 'regional alliances', 'regional companies', 'regional diplomacy', 'regulation', 'reionization',
    'religious tourism', 'remote work', 'rendition', 'renewable energy', 'reparations', 'reproductive rights', 'researchers', 'reshoring', 'resilient cities', 'resilient investing',
    'responsible ai', 'responsible tourism', 'restitution', 'retail', 'reverse logistics', 'revolution', 'reward modeling', 'rewilding', 'rhenium', 'rhodium',
    'ride sharing', 'right to repair', 'riots', 'risk management', 'robotics', 'robots', 'robust investing', 'rohingya crisis', 'rounds', 'route optimization',
    'royalty companies', 'rural tourism', 'ruthenium', 'safe exploration', 'safehaven investing', 'samarium', 'savings and loans', 'scams', 'scandal', 'scandium',
    'scholarships', 'schools', 'schrodingers cat', 'science diplomacy', 'scrap', 'seasonality', 'second amendment', 'secular companies', 'security', 'seed ai',
    'selective investing', 'selenium', 'selfdriving cars', 'senate', 'service learning', 'seti', 'sexual assault', 'shared mobility', 'shared prosperity', 'sharing economy',
    'sharp power', 'shell companies', 'shortonly investing', 'shortterm alliances', 'shuttle diplomacy', 'signals', 'silver', 'silver economy', 'simulation theory', 'singularity',
    'slow tourism', 'slum tourism', 'smallcap companies', 'smart cities', 'smart grid', 'smart grids', 'smart manufacturing', 'smart mobility', 'smart power', 'smelters',
    'sms marketing', 'smuggling', 'social commerce', 'social dividend', 'social marketing', 'social media', 'social mobility', 'social protection', 'social safety net', 'socialism',
    'soft actorcritic', 'soft power', 'soil erosion', 'solar energy', 'solar power', 'space race', 'space tourism', 'special education', 'specialty metals', 'speculators',
    'spinoff companies', 'spiritual tourism', 'splitoff companies', 'sponsored content', 'sponsorship', 'sponsorships', 'sports diplomacy', 'sports tourism', 'stackers', 'standard model',
    'star alliances', 'startup ecosystems', 'state building', 'static alliances', 'staycation', 'stealth marketing', 'steam education', 'stellarator', 'stem cell research', 'stem education',
    'stocks', 'strategic alliances', 'strategic investing', 'strategic metals', 'streaming', 'streaming companies', 'string landscape', 'string theory', 'stub companies', 'student loans',
    'students', 'subliminal messages', 'substance abuse', 'sudan coup', 'sudan revolution', 'summit diplomacy', 'supernova', 'supply chain', 'surveillance', 'survivalists',
    'sustainability', 'sustainable cities', 'sustainable finance', 'sustainable tourism', 'sustainable trade', 'symbiotic alliances', 'syndicates', 'synthetic biology', 'syrian civil war', 'tactical investing',
    'tantalum', 'tariffs', 'tax evasion', 'tax havens', 'taxes', 'teachers', 'technicians', 'technology metals', 'technology parks', 'telemarketing',
    'tellurium', 'temporary alliances', 'terbium', 'terrorism', 'testimonials', 'thorium', 'thulium', 'tieins', 'tigray war', 'timber trafficking',
    'time travel', 'tin', 'tissue engineering', 'titanium', 'tokamak', 'torture', 'tourism marketing', 'traceability', 'track two diplomacy', 'trade',
    'trade agreements', 'trade facilitation', 'trade finance', 'trade secrets', 'trade wars', 'trademarks', 'traders', 'trafficking', 'transfer learning', 'transgender',
    'transhumanism', 'transparency', 'travel ban', 'travel marketing', 'travel restrictions', 'treasury', 'trends', 'triple bottom line', 'tripwires', 'trusts',
    'truth commissions', 'tuberculosis', 'tungsten', 'ufo sightings', 'ukraine conflict', 'unemployment', 'ungoverned spaces', 'unions', 'united nations', 'universal education',
    'upstream alliances', 'urban air mobility', 'urban manufacturing', 'urban planning', 'urban sprawl', 'utility fog', 'vaccine diplomacy', 'vaccine hesitancy', 'vaccines', 'valuations',
    'value alignment', 'value companies', 'value extrapolation', 'value investing', 'value learning', 'values education', 'vanadium', 'veganism', 'vegetarianism', 'venezuela crisis',
    'vertical alliances', 'vertical farming', 'violent extremism', 'viral marketing', 'virtual goods', 'virtual integration', 'virtual reality', 'visa', 'visa policy', 'visionary companies',
    'voice commerce', 'volatility', 'volunteer tourism', 'voter suppression', 'voting', 'voting rights', 'wages', 'walkable cities', 'war', 'war crimes',
    'waste trafficking', 'water diplomacy', 'water justice', 'water scarcity', 'wealth gap', 'welfare', 'wellbeing economy', 'wellness tourism', 'whistleblowers', 'white economy',
    'white labeling', 'wildlife crime', 'wills', 'wind energy', 'wind power', 'winlose alliances', 'winwin alliances', 'woke', 'wordofmouth', 'workation',
    'worker cooperatives', 'workplace accidents', 'world bank', 'wto', 'xenotransplantation', 'yellow vests', 'yemen crisis', 'yemen war', 'ytterbium', 'yttrium',
    'zero waste', 'zeroshot learning', 'zerosum alliances', 'zinc', 'zirconium', 'zoning laws'
    ]
############

# default values
DEFAULT_OLDNESS_SECONDS = 120
DEFAULT_MAXIMUM_ITEMS = 25
DEFAULT_MIN_POST_LENGTH = 10
DEFAULT_DEFAULT_KEYWORD_WEIGHT_PICK = 0.15


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
]
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################


def delete_org_files_in_tmp():
    tmp_folder = "/tmp/"
    target_prefix = ".org"

    try:
        # Check if the /tmp/ folder exists
        if not os.path.exists(tmp_folder):
            logging.info(
                f"[DISK CLEANUP] Error: The directory '{tmp_folder}' does not exist."
            )
            return

        # Iterate through the files in /tmp/ folder
        for filename in os.listdir(tmp_folder):
            if filename.startswith(target_prefix):
                file_path = os.path.join(tmp_folder, filename)

                # Try to remove the file
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        logging.info(f"[DISK CLEANUP] Deleted file: {filename}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        logging.info(f"[DISK CLEANUP] Deleted directory: {filename}")

                # Handle permission errors and other exceptions
                except Exception as e:
                    logging.exception(f"[DISK CLEANUP] Error deleting {filename}: {e}")

    except Exception as e:
        logging.exception(f"[DISK CLEANUP] An error occurred: {e}")


def delete_core_files():
    current_folder = "/exorde/"
    target_prefix = "core."
    # delete all files in /exorde/ that are starting with core.* (no extension)
    try:
        # check if the /exorde/ folder exists
        if not os.path.exists(current_folder):
            logging.info(f"[DISK CLEANUP] Error: The directory '/exorde/' does not exist.")
            return
        
        # iterate through the files in /exorde/ folder
        for filename in os.listdir(current_folder):
            # find all files  starting with core.* (no extension), example core.4000 core.2315331 core.1
            if filename.startswith(target_prefix) and not filename.endswith(".json"):   
                file_path = os.path.join(current_folder, filename)
                # try to remove the file
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        logging.info(f"[DISK CLEANUP] Deleted file: {filename}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        logging.info(f"[DISK CLEANUP] Deleted directory: {filename}")
                # handle permission errors and other exceptions
                except Exception as e:
                    logging.exception(f"[DISK CLEANUP] Error deleting {filename}: {e}")

    except Exception as e:
        logging.exception(f"[DISK CLEANUP]An error occurred: {e}")


def cleanhtml(raw_html):
    """
    Clean HTML tags and entities from raw HTML text.

    Args:
        raw_html (str): Raw HTML text.

    Yields:
        str: Cleaned text without HTML tags and entities.
    """
    CLEANR = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    cleantext = re.sub(CLEANR, "", raw_html)
    return cleantext


def convert_datetime(datetime_str):
    datetime_str = str(datetime_str)
    dt = datett.strptime(datetime_str, "%Y-%m-%d %H:%M:%S%z")
    converted_str = dt.strftime("%Y-%m-%dT%H:%M:%S.00Z")
    return converted_str

########################################################################

def check_proxy_account_list():
    logging.basicConfig(level=logging.INFO)

    # Check if the file exists in the current directory
    if not os.path.exists("proxy_account_list.json"):
        logging.info("proxy_account_list.json not found in the current directory.")
        return False

    # Read the contents of the JSON file
    try:
        with open("proxy_account_list.json", "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        logging.info("proxy_account_list.json is not a valid JSON file.")
        return False

    # Check if the loaded data has the expected structure
    if "accounts" not in data or not isinstance(data["accounts"], list):
        logging.info("proxy_account_list.json does not have the expected structure.")
        return False

    num_accounts = len(data["accounts"])
    logging.info(
        f"[Twitter] [MULTI ACCOUNTS INIT] 'proxy_account_list.json' file OK - {num_accounts} accounts founds."
    )
    return True


def check_env():
    SCWEET_USERNAME = os.getenv("SCWEET_USERNAME", "")
    SCWEET_PASSWORD = os.getenv("SCWEET_PASSWORD", "")
    SCWEET_EMAIL = os.getenv("SCWEET_EMAIL", "")

    if (SCWEET_USERNAME != "" and SCWEET_PASSWORD != "" and SCWEET_EMAIL != ""):
        return True

    if check_proxy_account_list():
        return True
    # Check if the .env file exists
    if not os.path.exists(".env"):
        logging.info("[Twitter] Solo account mode - .env file does not exist.")
        return False

    # Read the .env file
    with open(".env", "r") as f:
        content = f.read()

    # Split the content into lines
    lines = content.split("\n")

    # Define a dictionary to hold the keys and values
    keys = {"SCWEET_EMAIL": None, "SCWEET_PASSWORD": None, "SCWEET_USERNAME": None}

    # Parse each line
    for line in lines:
        if "=" in line:
            key, value = line.split("=", 1)
            if key in keys and value != "":
                keys[key] = value

    # Check if all keys have non-null values
    for key in keys:
        if keys[key] is None:
            return False

    # If all checks pass, return True
    return True


#############################################################################
#############################################################################
#############################################################################

current_dir = Path(__file__).parent.absolute()

def load_env_variable(key, default_value=None, none_allowed=False):
    v = os.getenv(key, default=default_value)
    if v is None and not none_allowed:
        raise RuntimeError(f"{key} returned {v} but this is not allowed!")
    return v


def get_email(env):
    global _EMAIL
    dotenv.load_dotenv(env, verbose=True)
    default_var = load_env_variable("SCWEET_EMAIL", none_allowed=True)
    if _EMAIL is not None and len(_EMAIL) > 0:
        default_var = _EMAIL
    return default_var


def get_password(env):
    global _PASSWORD
    dotenv.load_dotenv(env, verbose=True)
    default_var = load_env_variable("SCWEET_PASSWORD", none_allowed=True)
    if _PASSWORD is not None and len(_PASSWORD) > 0:
        default_var = _PASSWORD
    return default_var


def get_username(env):
    global _USERNAME
    dotenv.load_dotenv(env, verbose=True)
    default_var = load_env_variable("SCWEET_USERNAME", none_allowed=True)
    if _USERNAME is not None and len(_USERNAME) > 0:
        default_var = _USERNAME
    return default_var


def get_proxy(env):
    global _PROXY
    dotenv.load_dotenv(env, verbose=True)
    default_var = load_env_variable("HTTP_PROXY", none_allowed=True)
    if _PROXY is not None and len(_PROXY) > 0:
        default_var = _PROXY
    return default_var


def get_data(card):
    """Extract data from tweet card"""
    image_links = []

    try:
        username = card.find_element(by=By.XPATH, value=".//span").text
    except:
        return

    try:
        handle = card.find_element(
            by=By.XPATH, value='.//span[contains(text(), "@")]'
        ).text
    except:
        return

    try:
        postdate = card.find_element(by=By.XPATH, value=".//time").get_attribute(
            "datetime"
        )
    except:
        return

    try:
        text = card.find_element(
            by=By.XPATH, value='.//div[@data-testid="tweetText"]'
        ).text
    except:
        text = ""

    try:
        embedded = card.find_element(by=By.XPATH, value=".//div[2]/div[2]/div[2]").text
    except:
        embedded = ""

    try:
        reply_cnt = card.find_element(
            by=By.XPATH, value='.//div[@data-testid="reply"]'
        ).text
    except:
        reply_cnt = 0

    try:
        retweet_cnt = card.find_element(
            by=By.XPATH, value='.//div[@data-testid="retweet"]'
        ).text
    except:
        retweet_cnt = 0

    try:
        like_cnt = card.find_element(
            by=By.XPATH, value='.//div[@data-testid="like"]'
        ).text
    except:
        like_cnt = 0

    try:
        elements = card.find_elements(
            by=By.XPATH,
            value='.//div[2]/div[2]//img[contains(@src, "https://pbs.twimg.com/")]',
        )
        for element in elements:
            image_links.append(element.get_attribute("src"))
    except:
        image_links = []

    try:
        promoted = (
            card.find_element(by=By.XPATH, value=".//div[2]/div[2]/[last()]//span").text
            == "Promoted"
        )
    except:
        promoted = False
    if promoted:
        return

    # get a string of all emojis contained in the tweet
    try:
        emoji_tags = card.find_elements(
            by=By.XPATH, value='.//img[contains(@src, "emoji")]'
        )
    except:
        return
    emoji_list = []
    for tag in emoji_tags:
        try:
            filename = tag.get_attribute("src")
            emoji = chr(
                int(re.search(r"svg\/([a-z0-9]+)\.svg", filename).group(1), base=16)
            )
        except AttributeError:
            continue
        if emoji:
            emoji_list.append(emoji)
    emojis = " ".join(emoji_list)

    # tweet url
    try:
        element = card.find_element(
            by=By.XPATH, value='.//a[contains(@href, "/status/")]'
        )
        tweet_url = element.get_attribute("href")
    except:
        return

    tweet = (
        username,
        handle,
        postdate,
        text,
        embedded,
        emojis,
        reply_cnt,
        retweet_cnt,
        like_cnt,
        image_links,
        tweet_url,
    )
    return tweet



def get_chrome_path():
    if os.path.isfile("/usr/bin/chromium-browser"):
        return "/usr/bin/chromium-browser"
    elif os.path.isfile("/usr/bin/chromium"):
        return "/usr/bin/chromium"
    elif os.path.isfile("/usr/bin/chrome"):
        return "/usr/bin/chrome"
    elif os.path.isfile("/usr/bin/google-chrome"):
        return "/usr/bin/google-chrome"
    else:
        return None



def verify_account_structure(account):
    required_keys = [
        "proxy",
        "proxy_username",
        "proxy_password",
        "proxy_port",
        "email",
        "password",
        "username",
        "last_used",
        "duration",
        "cookies_file",
    ]
    if not all(key in account for key in required_keys):
        logging.error("Account is missing required keys: %s", account)
        return False
    return True


def select_proxy_and_account_if_any():

    result_account = None
    try:
        # Attempt to open and read the "proxy_account_list.json" file
        with open(PROXY_ACCOUNT_MAP_FP, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error("[MULTI ACCOUNTS] File 'proxy_account_list.json' not found. - USING DEFAULT SOLO ACCOUNT MODE")
        return None
    except json.JSONDecodeError:
        logging.error("[MULTI ACCOUNTS] Error decoding 'proxy_account_list.json'.")
        return None

    logging.info("\n******************* ________ SELECTION - MULTI ACCOUNT MODE ________ ********************")

    # Check if the "data" is a dictionary and it contains the key "accounts"
    if not isinstance(data, dict) or "accounts" not in data:
        logging.error("[MULTI ACCOUNTS] 'proxy_account_list.json' does not have the expected structure.")
        return None

    # Extract the "accounts" list from the JSON data
    accounts = data["accounts"]

    # If the "accounts" list is empty, return None
    if not accounts:
        logging.warning("[MULTI ACCOUNTS] 'proxy_account_list.json' does not contain any accounts.")
        return None

    # Verify account structure and attributes
    for account in accounts:
        if not verify_account_structure(account):
            return None

    # Sort the accounts based on the "last_used" timestamp in descending order
    sorted_accounts = sorted(accounts, key=lambda x: x["duration"], reverse=True)
    oldest_used_accounts = sorted(accounts, key=lambda x: x["last_used"], reverse=True)

    # Get the parameters from the JSON data
    parameters = data.get("parameters", {})
    rotate_account_after_duration = parameters.get(
        "rotate_account_after_duration", 3600
    )

    # Iterate through the sorted accounts
    for account in sorted_accounts:
        if account["duration"] <= rotate_account_after_duration:
            logging.info(
                "[Twitter] [MULTI ACCOUNTS] _______ Rotation system: selected account '%s'. _______",
                account["username"],
            )
            account["last_used"] = int(time.time())
            result_account = account
            break
        elif account["duration"] <= rotate_account_after_duration:
            logging.info(
                "[Twitter] [MULTI ACCOUNTS] Using account '%s' as duration is less than rotate_account_after_duration.",
                account["username"],
            )
            account["last_used"] = int(time.time())
            result_account = account
            break

    if result_account is None:
        # If no suitable account is found, select the oldest account and reset its "last_used" timestamp
        oldest_account = oldest_used_accounts[-1]
        logging.info(
            "[Twitter] [MULTI ACCOUNTS] No suitable account found with duration <= %d. Selecting the oldest account: '%s' and reseting its duration.",
            rotate_account_after_duration,
            oldest_account["username"],
        )
        oldest_account["last_used"] = int(time.time())
        oldest_account["duration"] = 0  # reset this duration
        result_account = oldest_account

    # Write the updated data back to the account file
    try:
        with open(PROXY_ACCOUNT_MAP_FP, "w") as file:
            json.dump(data, file, indent=4)
    except IOError:
        logging.error(
            "[Twitter] [MULTI ACCOUNTS] Error writing to 'proxy_account_list.json'."
        )
        return

    # write
    return result_account


def update_proxy_account_map():
    global _EMAIL, _USERNAME, _PASSWORD, _COOKIE_FP, RATE_LIMITED, ITEMS_PRODUCED_SESSION
    logging.info(
        "[Twitter] [MULTI ACCOUNTS] Closing session: updating proxy_account_list.json file"
    )

    # Read the current data from the account file
    try:
        with open(PROXY_ACCOUNT_MAP_FP, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error(
            "[Twitter] [MULTI ACCOUNTS] File 'proxy_account_list.json' not found."
        )
        return
    except json.JSONDecodeError:
        logging.error(
            "[Twitter] [MULTI ACCOUNTS] Error decoding 'proxy_account_list.json'."
        )
        return
    now = int(time.time())
    duration_malus = 3 * 3600 if ( RATE_LIMITED or ITEMS_PRODUCED_SESSION == 0 ) else 0
    if RATE_LIMITED:
        logging.info(
            f"[Twitter] [MULTI ACCOUNTS]  Current worker seem rate limited or buggy, we add 3 hours to its counter, to wait."
        )
    for account in data["accounts"]:
        if account["email"] == _EMAIL:
            last_used = account["last_used"]
            if last_used == 0:
                last_used = now - 120
            new_duration = now - last_used + duration_malus + 60
            logging.info(
                f"[Twitter] [MULTI ACCOUNTS] -\tCurrent session duration: {new_duration} seconds"
            )
            if account["duration"] + new_duration:
                account["duration"] += new_duration
            account["cookies_file"] = _COOKIE_FP
            account["last_used"] = now
            break
    # Write the updated data back to the account file
    try:
        with open(PROXY_ACCOUNT_MAP_FP, "w") as file:
            json.dump(data, file, indent=4)
    except IOError:
        logging.error("Error writing to 'proxy_account_list.json'.")
        return


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""


def get_background_js(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS):

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (
        PROXY_HOST,
        PROXY_PORT,
        PROXY_USER,
        PROXY_PASS,
    )
    return background_js

class CriticalFailure(Exception):
    pass

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
def init_driver(
    headless=True, show_images=False, option=None, firefox=False, env=".env"
):
    """initiate a chromedriver or firefoxdriver instance
    --option : other option to add (str)
    """
    global driver, MULTI_ACCOUNT_MODE
    global _COOKIE_FP, _EMAIL, _USERNAME, _PASSWORD, _PROXY
    options = ChromeOptions()
    # driver_path = '/usr/local/bin/chromedriver'
    logging.info("Adding options to Chromium Driver")
    binary_path = get_chrome_path()
    options.binary_location = binary_path
    logging.info(f"\tSelected Chrome executable path = {binary_path}")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "--disable-blink-features"
    )  # Disable features that might betray automation
    # options.add_argument(
    #     "--disable-gpu"
    # )  # GPU rendering
    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )  # Disables a Chrome flag that shows an 'automation' toolbar
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation"]
    )  # Disable automation flags
    options.add_experimental_option(
        "useAutomationExtension", False
    )  # Disable automation extensions
    logging.info("\tDisable automation extensions & flags")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("user-data-dir=selenium")
    selected_user_agent = random.choice(user_agents)
    options.add_argument(f"user-agent={selected_user_agent}")
    logging.info("\tselected_user_agent :  %s", selected_user_agent)

    selected_proxy_account = select_proxy_and_account_if_any()
    if selected_proxy_account is not None:
            
        if headless is True:
            headless_mode = "--headless=new"
            options.add_argument(headless_mode)
            logging.info(f"\theadless mode used : {headless_mode}")

        MULTI_ACCOUNT_MODE = True
        _EMAIL = selected_proxy_account["email"]
        _USERNAME = selected_proxy_account["username"]
        _PASSWORD = selected_proxy_account["password"]
        _PROXY = selected_proxy_account["proxy"]
        PROXY_USERNAME = selected_proxy_account["proxy_username"]
        PROXY_PASSWORD = selected_proxy_account["proxy_password"]
        PROXY_PORT = selected_proxy_account["proxy_port"]
        _COOKIE_FP = selected_proxy_account["cookies_file"]
        if _COOKIE_FP is None or _COOKIE_FP == "":
            _COOKIE_FP = f"{_USERNAME}.pkl"

        pluginfile = "proxy_auth_plugin.zip"
        with zipfile.ZipFile(pluginfile, "w") as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr(
                "background.js",
                get_background_js(
                    PROXY_HOST=_PROXY,
                    PROXY_PORT=PROXY_PORT,
                    PROXY_USER=PROXY_USERNAME,
                    PROXY_PASS=PROXY_PASSWORD,
                ),
            )
        logging.info(f"[Twitter] [MULTI ACCOUNTS] adding PROXY extension: {pluginfile}")
        options.add_extension(pluginfile)

        logging.info(f"[Twitter] [MULTI ACCOUNTS] Selected Proxy: {_PROXY}")
        logging.info(
            f"[Twitter] [MULTI ACCOUNTS] Selected Account: {selected_proxy_account['email'], {selected_proxy_account['username']}, {print_first_and_last(selected_proxy_account['password'])}}"
        )
    else:        
        if headless is True:
            headless_mode = "--headless"
            options.add_argument(headless_mode)
            logging.info(f"\theadless mode used : {headless_mode}")

    options.add_argument("log-level=3")
    if show_images == False and firefox == False:
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
    if option is not None:
        options.add_argument(option)
    options.add_experimental_option("extensionLoadTimeout", 100000)
    try:
        ### DEBUGGING/DEVELOPMENT        
            # # Set up ChromeDriver
            # service = Service(ChromeDriverManager().install())
            
            # # Set up Chrome options
            # options = setup_chrome_options(bis_mode=True)  # Set to False to disable BIS mode        
            # Initialize the WebDriver
            # driver = webdriver.Chrome(service=service, options=options)
        ### DOCKER 
        driver_path = '/usr/local/bin/chromedriver'
        logging.info(f"Opening driver from path = {driver_path}")
        driver = webdriver.Chrome(service=Service(driver_path), options=options)
    except Exception as e:
        logging.exception("[TWITTER] [CRITICAL FAILURE] Failure to initialize the chrome driver")
        raise CriticalFailure("")
    if driver is None:        
        raise CriticalFailure("[TWITTER] [CRITICAL FAILURE] Failure to initialize the chrome driver")

    driver.set_page_load_timeout(8)
    return driver


def log_search_page(
    since,
    until_local,
    lang,
    display_type,
    word,
    to_account,
    from_account,
    mention_account,
    hashtag,
    filter_replies,
    proximity,
    geocode,
    minreplies,
    minlikes,
    minretweets,
):
    """ Search for this query between since and until_local"""
    global driver
    logging.info("Log search page =  %s", driver)
    # format the <from_account>, <to_account> and <hash_tags>
    from_account = (
        "(from%3A" + from_account + ")%20" if from_account is not None else ""
    )
    to_account = "(to%3A" + to_account + ")%20" if to_account is not None else ""
    mention_account = (
        "(%40" + mention_account + ")%20" if mention_account is not None else ""
    )
    hash_tags = "%20(%23" + hashtag + ")%20" if hashtag is not None else ""

    since = ""  # "since%3A" + since + "%20"

    if display_type == "Latest" or display_type == "latest":
        display_type = "&f=live"
    # proximity
    if proximity == True:
        proximity = "&lf=on"  # at the end
    else:
        proximity = ""

    path = (
        "https://x.com/search?q="
        + word
        + hash_tags
        + since
        + "&src=typed_query"
        + display_type
        + proximity
    )
    driver.get(path)
    sleep(1)

    if "i/flow/login" in driver.current_url:
        logging.info("[TWITTER] Problem detected, interrupting session early.")
        raise CriticalFailure("Problem detected, interrupting session early")
        
    return path


def type_slow(string, element):
    for character in str(string):
        element.send_keys(character)
        sleep(random.uniform(0.05, 0.27))


def print_first_and_last(s):
    if len(s) < 2:
        return s
    else:
        return s[0] + "***" + s[-1]


def check_and_kill_processes(process_names):
    for process_name in process_names:
        try:
            # Find processes by name
            result = subprocess.check_output(["pgrep", "-f", process_name])
            # If the previous command did not fail, we have some processes to kill
            if result:
                logging.info(f"[Chrome] Killing old processes for: {process_name}")
                subprocess.run(["pkill", "-f", process_name])
        except subprocess.CalledProcessError:
            # If pgrep fails to find any processes, it throws an error. We catch that here and assume no processes are running
            logging.info(f"[Chrome] No running processes found for: {process_name}")


def save_cookies(driver_):
    # Save cookies
    file_to_use = "cookies.pkl"
    if MULTI_ACCOUNT_MODE:
        if _COOKIE_FP is not None and len(_COOKIE_FP) > 0:
            file_to_use = _COOKIE_FP
    pickle.dump(driver_.get_cookies(), open(file_to_use, "wb"))
    logging.info(f"[Twitter Chrome] Saved cookies to {file_to_use}")


def clear_cookies():
    file_to_use = "cookies.pkl"
    if _COOKIE_FP is not None and len(_COOKIE_FP) > 0:
        file_to_use = _COOKIE_FP
    try:
        open(file_to_use, "wb").close()
        logging.info("Cleared cookies.")
    except Exception as e:
        logging.info("Clear cookies error: %s", e)


# URL API untuk mendapatkan kode 2FA
API_URL = "http://138.201.139.121:5000/confirmation_code"

def get_2fa_code(email):
    """Ambil kode 2FA dari API dengan maksimal 30 detik menunggu."""
    for _ in range(30):  # Coba selama 30 detik
        try:
            response = requests.get(API_URL, params={"to": email}, timeout=5)
            data = response.json()
            if "confirmation_code" in data:
                return data["confirmation_code"]
        except requests.RequestException as e:
            logging.error(f"Error request API: {e}")
        time.sleep(1)  # Tunggu 1 detik sebelum mencoba lagi
    return None  # Jika gagal mendapatkan kode

def log_in(env=".env", wait=1.2):
    global driver

    cookies_added = 0
    target_home_url = "https://x.com/home"
    target_home = "x.com/home"
    target_home_bis = "x.com/home"
    target_bis = "redirect_after_login=%2Fhome"
    
    driver.get("https://www.x.com/")
    sleep(1)
    
    try:
        # Load cookies if they exist
        SCWEET_COOKIES = os.getenv('SCWEET_COOKIES', None)
        if SCWEET_COOKIES:
            cookies = json.loads(SCWEET_COOKIES)
            logging.info('[Cookies] JSON-Loaded from env')
        else:
            try:
                file_to_use = "cookies.pkl"
                if _COOKIE_FP is not None and len(_COOKIE_FP) > 0:
                    file_to_use = _COOKIE_FP
                logging.info(f"[Cookies] Loading file: {file_to_use}")
                cookies = pickle.load(open(file_to_use, "rb"))
            except:
                cookies = []
                logging.info("[Cookies] File not found, no cookies.")

        logging.info("[Twitter Chrome] loading existing cookies...")
        for cookie in cookies:
            logging.info("\t-%s", cookie)
            if "expiry" in cookie and datett.fromtimestamp(cookie["expiry"]) < datett.now():
                logging.info("Cookie expired")
            else:
                try:
                    driver.add_cookie(cookie)
                    cookies_added += 1
                except exceptions.InvalidCookieDomainException as e:
                    logging.info("[Twitter Chrome] Not importable cookie: %s", e)
                except:
                    logging.info("[Twitter Chrome] Error for cookie %s", cookie)
        logging.info("[Twitter Chrome] Imported %s cookies.", cookies_added)
    except Exception as e:
        logging.exception("An error occurred retrieving cookies: %s", e)

    sleep(random.uniform(0, 1))
    driver.get(target_home_url)
    sleep(random.uniform(0, 1))
    
    email = get_email(env)
    password = get_password(env)
    username = get_username(env)

    logging.info("\t[Twitter] Email provided = %s", email)
    
    login_bar_found = False
    if check_exists_by_xpath('//a[@href="/login"]', driver):
        logging.info("[Twitter Chrome] Login bar at the bottom: Found")
        login_bar_found = True
    else:
        logging.info("[Twitter Chrome] Login bar at the bottom: Not Found")
    
    if not (target_home in driver.current_url or target_home_bis in driver.current_url) or login_bar_found:
        logging.info("[Twitter] Not on target, let's log in...")
        clear_cookies()
        driver.get("https://x.com/i/flow/login")

        email_xpath = '//input[@autocomplete="username"]'
        password_xpath = '//input[@autocomplete="current-password"]'
        username_xpath = '//input[@data-testid="ocfEnterTextTextInput"]'
        # XPath untuk input verifikasi 2FA. Perhatikan: pada kode contoh 2FA yang berhasil, input menggunakan name 'text'
        two_fa_xpath = "//input[@name='text']"  

        sleep(3)
        # Masukkan email
        logging.info("[Twitter Chrome] Current URL = %s", driver.current_url)
        logging.info("Entering Email..")
        email_el = driver.find_element(by=By.XPATH, value=email_xpath)
        type_slow(email, email_el)
        sleep(random.uniform(wait, wait + 1))
        email_el.send_keys(Keys.RETURN)
        sleep(random.uniform(wait, wait + 1))

        # Jika diminta username karena login activity tidak biasa
        if check_exists_by_xpath(username_xpath, driver):
            logging.info("Unusual Activity Mode")
            username_el = driver.find_element(by=By.XPATH, value=username_xpath)
            if username_el:
                logging.info("[Unusual Activity] found username element")
            sleep(random.uniform(wait, wait + 1))
            logging.info("Entering username..")
            type_slow(username, username_el)
            sleep(random.uniform(wait, wait + 1))
            username_el.send_keys(Keys.RETURN)
            sleep(random.uniform(wait, wait + 1))

        # Masukkan password
        password_el = driver.find_element(by=By.XPATH, value=password_xpath)
        if password_el:
            logging.info("[Login] found password element")
        logging.info("Entering password...")
        type_slow(password, password_el)
        sleep(random.uniform(wait, wait + 1))
        password_el.send_keys(Keys.RETURN)
        sleep(random.uniform(0, 1))
        
# Handle verifikasi 2FA jika form muncul
if check_exists_by_xpath(two_fa_xpath, driver):
    logging.info("[2FA] Kode verifikasi diminta, menunggu kode dari API...")
    code_input = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, two_fa_xpath))
    )
    code = get_2fa_code(email)
    if code:
        driver.execute_script("arguments[0].click();", code_input)
        code_input.send_keys(code)
        code_input.send_keys(Keys.ENTER)
        logging.info(f"[2FA] Kode verifikasi {code} dimasukkan...")
    else:
        logging.error(f"[2FA] Gagal mendapatkan kode 2FA untuk {email}.")
        code_manual = input("[2FA] Masukkan kode secara manual: ")
        driver.execute_script("arguments[0].click();", code_input)
        code_input.send_keys(code_manual)
        code_input.send_keys(Keys.ENTER)
    # Tambahkan delay ekstra agar sistem punya waktu untuk memproses login
    sleep(5)
    # Tunggu hingga redirect ke halaman home
    try:
        WebDriverWait(driver, 15).until(EC.url_contains("/home"))
        logging.info("[Twitter Login] Redirect ke halaman home berhasil.")
    except Exception as e:
        logging.error("Gagal mengalihkan ke halaman home setelah 2FA: %s", e)
else:
    logging.info("Verifikasi 2FA tidak diperlukan...")


        # Finalisasi login: arahkan ke halaman home
        driver.get(target_home_url)
        sleep(random.uniform(1, 1))
        logging.info("[Twitter Login] Current URL after login = %s", str(driver.current_url))
        if target_home in driver.current_url or target_home_bis in driver.current_url:
            logging.info("[Twitter Login] Success!")
            save_cookies(driver)
    else:
        logging.info("[Twitter] We are already logged in")



def is_within_timeframe_seconds(dt_str, timeframe_sec):
    # Convert the datetime string to a datetime object
    dt = datett.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Make it aware about timezone (UTC)
    dt = dt.replace(tzinfo=timezone.utc)

    # Get the current datetime in UTC
    current_dt = datett.now(timezone.utc)

    # Calculate the time difference between the two datetimes
    time_diff = current_dt - dt

    # Check if the time difference is within the specified timeframe in seconds
    if abs(time_diff) <= timedelta(seconds=timeframe_sec):
        return True
    else:
        return False


class RateLimited(Exception):
    def __init__(self, message="Rate limit exceeded"):
        self.message = message
        super().__init__(self.message)


max_old_tweets_successive = 2


def keep_scroling(
    data,
    tweet_ids,
    scrolling,
    tweet_parsed,
    limit,
    scroll,
    last_position,
    save_images=False,
):
    """ scrolling function for tweets crawling"""
    global driver, MAX_EXPIRATION_SECONDS, RATE_LIMITED

    save_images_dir = "/images"
    if save_images == True:
        if not os.path.exists(save_images_dir):
            os.mkdir(save_images_dir)

    rate_limitation = False
    successsive_old_tweets = 0
    while scrolling and tweet_parsed < limit:
        sleep(random.uniform(0.5, 1.5))
        # get the card of tweets
        page_cards = driver.find_elements(
            by=By.XPATH, value='//article[@data-testid="tweet"]'
        )  # changed div by article
        logging.info("[XPath] page cards found = %s", len(page_cards))
        if len(page_cards) == 0 and False:
            # check if we are rate-limited
            try:
                # wait for the popup to become visible, up to 4s (1.5s delay + 3.5s visibility)
                wait = WebDriverWait(driver, 4)
                element = wait.until(
                    lambda x: x.find_element(
                        By.XPATH, '//*[contains(text(),"Sorry, you are rate limited")]'
                    )
                    or x.find_element(
                        By.CLASS_NAME,
                        "css-1dbjc4n r-1awozwy r-1kihuf0 r-l5o3uw r-z2wwpe r-18u37iz r-1wtj0ep r-zd98yo r-xyw6el r-105ug2t",
                    )
                )

                # if we found the element, print that it was found
                logging.info(
                    "********\n********\n********\n\t\tYOUR TWITTER ACCOUNT IS NOW RATE LIMITED\n\n********\n********\n********"
                )
                rate_limitation = True
                RATE_LIMITED = True
                raise RateLimited("Twitter Account Viewing Rate Limit Exceeded")

                return (
                    data,
                    tweet_ids,
                    scrolling,
                    tweet_parsed,
                    scroll,
                    last_position,
                    rate_limitation,
                )
            except Exception as e:
                logging.info(
                    "[XPath] Rate limitation - can't find any error popup - %s", e
                )
        for card in page_cards:
            tweet = get_data(card)
            logging.debug("[XPath] Tweet visible currently = %s", len(page_cards))
            if tweet:
                try:
                    # check if the tweet is unique
                    # tweet_id = "".join(tweet[:-2])
                    tweet_id = "".join(str(item) for item in tweet[:-2])
                    last_date = str(tweet[2])
                    if tweet_id not in tweet_ids:
                        if is_within_timeframe_seconds(last_date, MAX_EXPIRATION_SECONDS):
                            tweet_ids.add(tweet_id)
                            data.append(tweet)
                            logging.info(f"[Tweet] Date = {last_date}")
                            logging.info("[Twitter Selenium] Found Tweet:  %s", tweet)
                            tweet_parsed += 1
                            successsive_old_tweets = 0
                        else:
                            logging.info("[Twitter Selenium] Old Tweet:  %s", tweet[3])
                            successsive_old_tweets += 1
                        if (
                            successsive_old_tweets >= max_old_tweets_successive
                            or tweet_parsed >= limit
                        ):
                            return (
                                data,
                                tweet_ids,
                                scrolling,
                                tweet_parsed,
                                scroll,
                                last_position,
                                rate_limitation,
                            )
                except Exception as e:
                    logging.exception(f"[Twitter] Error during tweet extraction: {e}")
        scroll_attempt = 0
        while tweet_parsed < limit:
            # check scroll position
            scroll += 1
            sleep(random.uniform(0.5, 1.5))
            # get current position and total scroll height
            curr_position = driver.execute_script("return window.pageYOffset;")
            total_height = driver.execute_script("return document.body.scrollHeight;")

            # scroll to a random position between current position and total height
            random_scroll_position = random.uniform(curr_position, total_height)
            logging.info("Scrolling %s", str(random_scroll_position))
            driver.execute_script(f"window.scrollTo(0, {random_scroll_position});")
            # driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1
                # end of scroll region
                if scroll_attempt >= 2:
                    scrolling = False
                    break
                else:
                    sleep(random.uniform(0.3, 1.4))  # attempt another scroll
            else:
                last_position = curr_position
                break
    return (
        data,
        tweet_ids,
        scrolling,
        tweet_parsed,
        scroll,
        last_position,
        rate_limitation,
    )


def check_exists_by_link_text(text, driver):
    try:
        driver.find_element_by_link_text(text)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_xpath(xpath, driver):
    timeout = 3
    try:
        driver.find_element(by=By.XPATH, value=xpath)
    except NoSuchElementException:
        return False
    return True


def extract_tweet_info(tweet_tuple):
    content = tweet_tuple[3]
    author = tweet_tuple[0]
    created_at = tweet_tuple[2]
    title = tweet_tuple[0]
    domain = "x.com"
    url = tweet_tuple[-1]
    external_id = url.split("/")[
        -1
    ]  # This assumes that the tweet ID is always the last part of the URL.

    return content, author, created_at, title, domain, url, external_id


async def scrape_(
    until=None,
    keyword="bitcoin",
    to_account=None,
    from_account=None,
    mention_account=None,
    interval=5,
    lang=None,
    limit=float("inf"),
    display_type="latest",
    hashtag=None,
    max_items_to_collect=20,
    filter_replies=False,
    proximity=False,
    max_search_page_tries=1,
    geocode=None,
    minreplies=None,
    minlikes=None,
    minretweets=None,
) -> AsyncGenerator[Item, None]:
    """
    Asynchronously scrape data from twitter using requests, starting from <since> until <until>. The program make a search between each <since> and <until_local>
    until it reaches the <until> date if it's given, else it stops at the actual date.

    Yields:
    Item: containing all tweets scraped with the associated features.
    """
    global driver
    global status_rate_limited
    global ITEMS_PRODUCED_SESSION
    if status_rate_limited:
        logging.debug(
            "[Twitter Status: Rate limited] Preventingly not starting scraping."
        )
        return
        yield

    if driver is None:
        raise CriticalFailure("Driver is not initialized properly!")

    logging.info("\tScraping latest tweets on keyword =  %s", keyword)
    # ------------------------- Variables :
    # list that contains all data
    data = []
    # unique tweet ids
    tweet_ids = set()
    # start scraping from <since> until <until>
    since = datetime.date.today().strftime("%Y-%m-%d")
    # add the <interval> to <since> to get <until_local> for the first refresh
    until_local = datetime.datetime.strptime(since, "%Y-%m-%d") + datetime.timedelta(
        days=interval
    )
    # if <until>=None, set it to the actual date
    if until is None:
        until = datetime.date.today().strftime("%Y-%m-%d")
    since = until
    # set refresh at 0. we refresh the page for each <interval> of time.
    refresh = 0

    # ------------------------- start scraping : keep searching until until
    # open the file
    logging.info("\tStart collecting tweets....")
    nb_search_tries = 0
    # log search page for a specific <interval> of time and keep scrolling unltil scrolling stops or reach the <until>
    while True:
        if (
            nb_search_tries >= max_search_page_tries
            or len(data) >= max_items_to_collect
        ):
            break

        scroll = 0
        if type(since) != str:
            since = datetime.datetime.strftime(since, "%Y-%m-%d")
        if type(until_local) != str:
            until_local = datetime.datetime.strftime(until_local, "%Y-%m-%d")

        # logging.info("Start log_search_page....")
        nb_search_tries += 1

        path = log_search_page(
            word=keyword,
            since=since,
            until_local=until_local,
            to_account=to_account,
            from_account=from_account,
            mention_account=mention_account,
            hashtag=hashtag,
            lang=lang,
            display_type=display_type,
            filter_replies=filter_replies,
            proximity=proximity,
            geocode=geocode,
            minreplies=minreplies,
            minlikes=minlikes,
            minretweets=minretweets,
        )
        refresh += 1
        # logging.info("Start execute_script....")
        last_position = driver.execute_script("return window.pageYOffset;")
        scrolling = True
        # logging.info("looking for tweets between " + str(since) + " and " + str(until_local) + " ...")
        logging.info("\tURL being parsed :  %s", str(path))
        tweet_parsed = 0
        sleep(random.uniform(0.5, 1.5))
        # logging.info("Start scrolling & get tweets....")
        (
            data,
            tweet_ids,
            scrolling,
            tweet_parsed,
            scroll,
            last_position,
            rate_limited,
        ) = keep_scroling(
            data, tweet_ids, scrolling, tweet_parsed, limit, scroll, last_position
        )
        if rate_limited:
            logging.info("[Twitter Status: Rate limited] Stopping scraping.")
            status_rate_limited = True
            break

        if scroll > 50:
            logging.debug("\tReached 50 scrolls: breaking")
            break
        if type(since) == str:
            since = datetime.datetime.strptime(since, "%Y-%m-%d") + datetime.timedelta(
                days=interval
            )
        else:
            since = since + datetime.timedelta(days=interval)
        if type(since) != str:
            until_local = datetime.datetime.strptime(
                until_local, "%Y-%m-%d"
            ) + datetime.timedelta(days=interval)
        else:
            until_local = until_local + datetime.timedelta(days=interval)

        for tweet_tuple in data:
            # ex: ('xxxxx', '@xxxx', '2023-06-16T10:10:59.000Z',
            # 'xx\n@xxxx\n·\nJun 16', '#Criptomoedas #Bitcoin\nNesta quinta-feira, 15,
            # a BlackRock solicitou a autorização para ofertar um fundo negociado em bolsa (ETF) de bitcoin nos Estados Unidos.\nSe aprovado, o
            # ETF será o primeiro dos Estados Unidos de bitcoin à vista.', '', '1', '', '1',
            # ['https://pbs.twimg.com/card_img/12.21654/zd45zz5?format=jpg&name=small'], 'https://x.com/xxxxx/status/1231456479')
            # Create a new sha1 hash
            (
                content_,
                author_,
                created_at_,
                title_,
                domain_,
                url_,
                external_id_,
            ) = extract_tweet_info(tweet_tuple)
            if (
                keyword.lower() in author_.lower()
                and not keyword.lower() in content_.lower()
            ):
                logging.info(
                    "Keyword not found in text, but in author's name, skipping this false positive."
                )
                continue
            sha1 = hashlib.sha1()
            # Update the hash with the author string encoded to bytest
            try:
                author_ = author_
            except:
                author_ = "unknown"
            sha1.update(author_.encode())
            author_sha1_hex = sha1.hexdigest()

            new_tweet_item = Item(
                content=Content(content_),
                author=Author(author_sha1_hex),
                created_at=CreatedAt(created_at_),
                domain=Domain(domain_),
                url=Url(url_),
                external_id=ExternalId(external_id_),
            )
            ITEMS_PRODUCED_SESSION += 1
            yield new_tweet_item


#############################################################################
#############################################################################
#############################################################################
def convert_spaces_to_percent20(input_string):
    return input_string.replace(" ", "%20")

def read_parameters(parameters):
    # Check if parameters is not empty or None
    if parameters and isinstance(parameters, dict):
        try:
            max_oldness_seconds = parameters.get(
                "max_oldness_seconds", DEFAULT_OLDNESS_SECONDS
            )
        except KeyError:
            max_oldness_seconds = DEFAULT_OLDNESS_SECONDS

        try:
            maximum_items_to_collect = parameters.get(
                "maximum_items_to_collect", DEFAULT_MAXIMUM_ITEMS
            )
        except KeyError:
            maximum_items_to_collect = DEFAULT_MAXIMUM_ITEMS

        try:
            min_post_length = parameters.get("min_post_length", DEFAULT_MIN_POST_LENGTH)
        except KeyError:
            min_post_length = DEFAULT_MIN_POST_LENGTH

        try:
            pick_default_keyword_weight = parameters.get(
                "pick_default_keyword_weight", DEFAULT_DEFAULT_KEYWORD_WEIGHT_PICK
            )
        except KeyError:
            pick_default_keyword_weight = DEFAULT_DEFAULT_KEYWORD_WEIGHT_PICK
    else:
        # Assign default values if parameters is empty or None
        max_oldness_seconds = DEFAULT_OLDNESS_SECONDS
        maximum_items_to_collect = DEFAULT_MAXIMUM_ITEMS
        min_post_length = DEFAULT_MIN_POST_LENGTH
        pick_default_keyword_weight = DEFAULT_DEFAULT_KEYWORD_WEIGHT_PICK

    return (
        max_oldness_seconds,
        maximum_items_to_collect,
        min_post_length,
        pick_default_keyword_weight,
    )

def fetch_keywords_list() -> list:
    # Fetch the list of keywords from the online source, ONLINE_KW_LIST_URL
    try:
        # remote file is a list of comma-separated keywords
        response = requests.get(ONLINE_KW_LIST_URL, timeout=1)
        if response.status_code == 200:
            keywords_list = response.text.split(",")
            # remove any empty strings, and strip leading/trailing whitespace, and \n
            keywords_list = [kw.strip() for kw in keywords_list if kw.strip()]
            
            return keywords_list
    except Exception as e:
        logging.error(f"Failed to fetch keywords list: {e}")
        return None
    
async def query(parameters: dict) -> AsyncGenerator[Item, None]:
    global driver, MAX_EXPIRATION_SECONDS, status_rate_limited

    ## Deleting chromium tmp files taking up space
    try:
        delete_org_files_in_tmp()
    except Exception as e:
        logging.exception(f"[Twitter init cleanup] failed: {e}")
    try:
        delete_core_files()
    except Exception as e:
        logging.exception(f"[Twitter core. files cleanup] failed: {e}")


    # forced_update()
    (
        max_oldness_seconds,
        maximum_items_to_collect,
        min_post_length,
        pick_default_keyword_weight,
    ) = read_parameters(parameters)
    maximum_items_to_collect_special_check = 10
    MAX_EXPIRATION_SECONDS = max_oldness_seconds
    try:
        logging.info(f"[Twitter parameters] checking url_parameters: %s", parameters)
        if "url_parameters" in parameters and "keyword" in parameters["url_parameters"]:
            search_keyword = parameters["url_parameters"]["keyword"]
        if "keyword" in parameters:
            logging.info(f"[Twitter parameters] checking url_parameters... ")
            search_keyword = parameters["keyword"]
    except Exception as e:
        logging.exception(f"[Twitter parameters] Keyword input read failed: {e}")

    
    # try fetching from the online source
    try:
        logging.info(f"[Twitter] fetching keywords list from {ONLINE_KW_LIST_URL}")
        keywords_list = fetch_keywords_list()
    except Exception as e:
        logging.exception(f"[Twitter] Keywords list fetch failed: {e}")
        keywords_list = None

    if keywords_list is not None and keywords_list != []:
        search_keyword = random.choice(keywords_list)
        logging.info(f"[Twitter parameters] using online keyword: {search_keyword}")
        # if it fails, use a base keyword
    else:
        search_keyword = None

    if (
        search_keyword is None
        or len(search_keyword) < 1
        or random.random() < pick_default_keyword_weight
    ):
        search_keyword = random.choice(SPECIAL_KEYWORDS_LIST)

    search_keyword = convert_spaces_to_percent20(search_keyword)
    logging.info("[Twitter] internal Keyword used = %s", search_keyword)
    logging.getLogger("selenium").setLevel(logging.WARNING)
    select_login_based_scraper = False
    if check_env():
        select_login_based_scraper = True
    if select_login_based_scraper:
        # Selenium track A: login based
        try:
            try:
                check_and_kill_processes(["chromium", "chromedriver", "google-chrome"])
            except Exception as e:
                logging.info("[Twitter] [Kill old chromium processes] Error: %s", e)
            try:
                logging.info("[Twitter] Open driver")
                driver = init_driver(headless=True, show_images=False)
                logging.info("[Twitter] Chrome Selenium Driver =  %s", driver)
                logging.info("[Twitter] ------------- Trying to log in...")
                log_in()
                logging.info("[Twitter] Logged in.")
                save_cookies(driver)
            except CriticalFailure as e:
                 logging.info("[Twitter] Critical failure:  %s", e)
            except Exception as e:
                logging.info("[Twitter] Exception during Twitter Init:  %s", e)

            try:
                async for result in scrape_(
                    keyword=search_keyword,
                    display_type="latest",
                    limit=maximum_items_to_collect,
                ):
                    yield result
                if special_mode:
                    logging.info(
                        "[Twitter] Checking %s special keywords",
                        NB_SPECIAL_CHECKS,
                    )
                    for _ in range(NB_SPECIAL_CHECKS):
                        
                        if keywords_list is not None and keywords_list != []:
                            search_keyword = random.choice(keywords_list)
                            logging.info(f"[Twitter parameters] using online keyword: {search_keyword}")
                            # if it fails, use a base keyword
                        else:
                            search_keyword = random.choice(SPECIAL_KEYWORDS_LIST)
                        search_keyword = convert_spaces_to_percent20(search_keyword)
                        logging.info(
                            "[Twitter] [Special] Looking at keyword: %s",
                            search_keyword,
                        )
                        async for result in scrape_(
                            keyword=search_keyword,
                            display_type="latest",
                            limit=maximum_items_to_collect_special_check,
                        ):
                            yield result
            except Exception as e:
                logging.info("Failed to scrape tweets. Error =  %s", e)
                pass
        except CriticalFailure as e:
            logging.exception("[Twitter] CriticalFailure during execution =  %s", e)
            pass
        except Exception as e:
            logging.exception("[Twitter] Exception in during execution =  %s", e)
        finally:
            try:
                if MULTI_ACCOUNT_MODE:
                    logging.info("[Twitter] [MULTI ACCOUNTS] Finalization process")
                    # UPDATE ACCOUNT/PROXY METADATA
                    update_proxy_account_map()
                    if driver is not None:
                        logging.info("[Twitter] Close driver")
                        driver.close()
                        sleep(3)  # the 3 seconds rule
                        logging.info("[Twitter] Quit driver")
                        driver.quit()
                logging.info("[Twitter] End.")
                    
            except Exception as e:
                logging.exception(
                    "[Twitter Driver] Exception while closing/quitting driver =  %s", e
                )

    else:
        logging.info(
            "[Twitter] You must provide the necessary credentials to use the Twitter scraper."
        )
