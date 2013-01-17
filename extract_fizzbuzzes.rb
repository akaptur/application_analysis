working_dir = ARGV[0]
unless working_dir.end_with?('/')
  working_dir += '/'
end

require './config/environment'

apps = Application.all
apps = apps[apps.length - 20, apps.length]
File.open(working_dir+'appdata.json', 'w'){ |file|
  file.write(apps.to_json)}
