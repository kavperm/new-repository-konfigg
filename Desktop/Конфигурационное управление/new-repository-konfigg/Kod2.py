import sys
import xml.etree.ElementTree as ET
import urllib.request
import ssl

# Отключаем проверку SSL
ssl._create_default_https_context = ssl._create_unverified_context

# Этап 1: Чтение конфигурации
try:
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    
    config = {}
    for elem in root:
        config[elem.tag] = elem.text
    
    print("Параметры:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
except Exception as e:
    print(f"Ошибка конфигурации: {e}")
    sys.exit(1)

# Этап 2: Получение зависимостей Maven
try:
    group, artifact, version = config['package_name'].split(':')
    url = f"{config['repository_url']}/{group.replace('.', '/')}/{artifact}/{version}/{artifact}-{version}.pom"
    
    with urllib.request.urlopen(url) as response:
        pom_content = response.read()
    
    root = ET.fromstring(pom_content)
    namespace = {'maven': 'http://maven.apache.org/POM/4.0.0'}
    
    dependencies = []
    for dep in root.findall('.//maven:dependency', namespace):
        group_elem = dep.find('maven:groupId', namespace)
        artifact_elem = dep.find('maven:artifactId', namespace)
        
        if group_elem is not None and artifact_elem is not None:
            dep_string = f"{group_elem.text}:{artifact_elem.text}"
            dependencies.append(dep_string)
    
    print(f"\nПрямые зависимости {config['package_name']}:")
    for dep in dependencies:
        print(f"  {dep}")

    # Этап 3: Визуализация
    mermaid_code = f"graph TD\n    {config['package_name'].replace(':', '_')}[\"{config['package_name']}\"]\n"
    for dep in dependencies:
        dep_id = dep.replace(':', '_')
        mermaid_code += f"    {dep_id}[\"{dep}\"]\n    {config['package_name'].replace(':', '_')} --> {dep_id}\n"
    
    with open(config['output_filename'].replace('.png', '.mmd'), 'w') as f:
        f.write(mermaid_code)
    

    min_width = 2000
    width_per_dep = 400 
    svg_width = max(min_width, len(dependencies) * width_per_dep)
    svg_height = 300
    
    svg_content = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
<rect width="100%" height="100%" fill="white"/>
<text x="{svg_width//2}" y="50" text-anchor="middle" font-family="Arial" font-size="14">{config["package_name"]}</text>
'''
    
    if dependencies:
        spacing = svg_width / (len(dependencies) + 1)
        
        for i, dep in enumerate(dependencies):
            x = spacing * (i + 1)
            y = 200 
            svg_content += f'<line x1="{svg_width//2}" y1="70" x2="{x}" y2="180" stroke="black"/>\n'
            svg_content += f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial" font-size="12">{dep}</text>\n'
    
    svg_content += '</svg>'
    
    with open(config['output_filename'].replace('.png', '.svg'), 'w') as f:
        f.write(svg_content)
    
    print(f"\nMermaid схема сохранена в {config['output_filename'].replace('.png', '.mmd')}")
    print(f"SVG граф сохранен в {config['output_filename'].replace('.png', '.svg')}")

except Exception as e:
    print(f"Ошибка: {e}")