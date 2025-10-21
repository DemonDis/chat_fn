import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class HydraAIClient:
    def __init__(self, api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL")):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.working_endpoint = "/chat/completions"
    
    def chat_completion(self, messages, tools=None, model="gpt-4o-mini"):
        """Основной метод для общения с API с поддержкой функций"""
        url = self.base_url + self.working_endpoint
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        # Добавляем инструменты, если они предоставлены
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Ошибка API: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Ошибка запроса: {e}")
            return None

# Реализация внешних инструментов (функций)
class ToolManager:
    def __init__(self):
        self.available_tools = self._define_tools()
    
    def _define_tools(self):
        """Определяем доступные функции для модели"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Получить текущую погоду в указанном городе",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "Город и страна, например, Москва, Россия",
                            },
                            "unit": {
                                "type": "string", 
                                "enum": ["celsius", "fahrenheit"],
                                "description": "Единица измерения температуры",
                            }
                        },
                        "required": ["location"],
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate_math_expression",
                    "description": "Вычислить математическое выражение",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Математическое выражение для вычисления, например, '2 + 2 * 3'",
                            }
                        },
                        "required": ["expression"],
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_current_time",
                    "description": "Получить текущее время в указанном городе",
                    "parameters": {
                        "type": "object", 
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "Город для получения времени, например, 'Лондон' или 'Москва'",
                            }
                        },
                        "required": ["location"],
                    },
                }
            }
        ]
    
    def execute_tool(self, tool_name, arguments):
        """Выполняет указанную функцию с аргументами"""
        if tool_name == "get_current_weather":
            return self._get_weather(arguments)
        elif tool_name == "calculate_math_expression":
            return self._calculate_math(arguments)
        elif tool_name == "get_current_time":
            return self._get_time(arguments)
        else:
            return f"Функция {tool_name} не найдена"
    
    def _get_weather(self, args):
        """Имитация получения погоды (в реальности был бы вызов API погоды)"""
        location = args.get("location", "Неизвестно")
        unit = args.get("unit", "celsius")
        
        # Имитация данных погоды
        weather_data = {
            "Москва, Россия": {"temp": -5, "condition": "снег", "humidity": 85},
            "Лондон, Великобритания": {"temp": 8, "condition": "дождь", "humidity": 90},
            "Нью-Йорк, США": {"temp": 15, "condition": "ясно", "humidity": 65},
            "Токио, Япония": {"temp": 12, "condition": "облачно", "humidity": 70}
        }
        
        if location in weather_data:
            data = weather_data[location]
            return f"Погода в {location}: {data['temp']}°C, {data['condition']}, влажность {data['humidity']}%"
        else:
            return f"Погода для {location}: данные временно недоступны"
    
    def _calculate_math(self, args):
        """Вычисляет математическое выражение"""
        expression = args.get("expression", "")
        try:
            # ВНИМАНИЕ: В продакшене используйте безопасные методы вычисления!
            result = eval(expression)
            return f"Результат: {expression} = {result}"
        except Exception as e:
            return f"Ошибка вычисления: {e}"
    
    def _get_time(self, args):
        """Имитация получения времени (в реальности был бы вызов API времени)"""
        location = args.get("location", "Неизвестно")
        
        time_data = {
            "Москва": "15:30 (MSK)",
            "Лондон": "12:30 (GMT)", 
            "Нью-Йорк": "07:30 (EST)",
            "Токио": "21:30 (JST)"
        }
        
        if location in time_data:
            return f"Текущее время в {location}: {time_data[location]}"
        else:
            return f"Время для {location}: данные временно недоступны"

def main():
    client = HydraAIClient()
    tool_manager = ToolManager()
    
    messages = [
        {
            "role": "system", 
            "content": """Ты - полезный AI-ассистент, который умеет вызывать внешние инструменты.
Если пользователь спрашивает о погоде, времени или нужно вычислить математическое выражение - используй соответствующие функции.
После получения результатов функций - предоставь пользователю красивый оформленный ответ."""
        }
    ]
    
    print("=== Hydra AI Чат-бот с вызовом функций ===")
    print("✅ Реализовано по заданию: вызов внешних инструментов")
    print("Доступные функции:")
    print("  - get_current_weather: получение погоды")
    print("  - calculate_math_expression: вычисления")  
    print("  - get_current_time: получение времени")
    print("\nНапишите 'выход' для завершения.\n")
    
    # Первый запрос с информацией о функциях
    use_tools = True
    
    while True:
        user_input = input("👤 Пользователь: ")
        if user_input.lower() in ['выход', 'exit', 'quit']:
            break
            
        messages.append({"role": "user", "content": user_input})
        
        # Шаг 1: Отправляем запрос к модели с информацией о функциях
        response_data = client.chat_completion(
            messages=messages, 
            tools=tool_manager.available_tools if use_tools else None,
            model="gpt-4o-mini"
        )
        
        if not response_data:
            print("❌ Ошибка: не удалось получить ответ от API")
            messages.pop()
            continue
        
        # После первого запроса больше не отправляем tools (если не нужно)
        use_tools = False
        
        response_message = response_data["choices"][0]["message"]
        
        # Шаг 2: Проверяем, хочет ли модель вызвать функцию
        if "tool_calls" in response_message and response_message["tool_calls"]:
            print("🔄 Ассистент вызывает внешнюю функцию...")
            
            # Добавляем сообщение с вызовом функции в историю
            messages.append(response_message)
            
            # Обрабатываем каждый вызов функции
            for tool_call in response_message["tool_calls"]:
                function_name = tool_call["function"]["name"]
                function_args = json.loads(tool_call["function"]["arguments"])
                
                print(f"   📞 Вызов функции: {function_name} с аргументами: {function_args}")
                
                # Выполняем функцию
                function_response = tool_manager.execute_tool(function_name, function_args)
                
                print(f"   📊 Результат функции: {function_response}")
                
                # Добавляем результат функции в историю
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": function_response,
                })
            
            # Шаг 3: Отправляем историю с результатами функций обратно в модель
            second_response = client.chat_completion(messages=messages)
            
            if second_response:
                final_message = second_response["choices"][0]["message"]
                assistant_reply = final_message["content"]
                print(f"🤖 Ассистент: {assistant_reply}")
                messages.append(final_message)
            else:
                print("❌ Ошибка при получении финального ответа")
                
        else:
            # Обычный текстовый ответ
            assistant_reply = response_message["content"]
            print(f"🤖 Ассистент: {assistant_reply}")
            messages.append(response_message)

if __name__ == "__main__":
    main()
