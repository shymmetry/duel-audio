import subprocess

def get_audio_devices_with_ids():
    try:
        ps_script = r"""
        $base = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio\Render"
        $property_key = "{a45c254e-df1c-4efd-8020-67d146a850e0},2"
        Get-ChildItem -Path $base | ForEach-Object {
            $guid = $_.PSChildName
            $property_path = "$base\$guid\Properties"
            $name = (Get-ItemProperty -Path $property_path -Name $property_key).$property_key
            "$name::{0.0.0.00000000}.$guid"
        }
        """

        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=5
        )

        lines = result.stdout.strip().splitlines()

        device_map = {}
        for line in lines:
            if "::" in line:
                name, guid = line.strip().split("::", 1)
                device_map[name.strip()] = guid.strip()

        return device_map

    except subprocess.TimeoutExpired:
        print("Timeout fetching audio devices.")
        return {}
    except Exception as e:
        print("Error fetching audio device IDs:", e)
        return {}