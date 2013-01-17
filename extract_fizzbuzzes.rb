working_dir = ARGV[0]
unless working_dir.end_with?('/')
  working_dir += '/'
end

require './config/environment'

apps = Application.all
last_apps = apps[apps.length - 20, apps.length]
last_apps.each do |app|
  File.open(working_dir+app.id.to_s+'.txt', 'w'){ |file|
    file.write(app.fizzbuzz)}
end