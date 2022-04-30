from serializer import get_serializer
import argparse


def serializer():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-s", "--source", type=str, help="Path to source file")
    arg_parser.add_argument("-f", "--format", type=str, help="Final format: json, toml or yaml")
    arg_parser.add_argument("-r", "--result-file", type=str, help="Path to file to save result.")

    args = arg_parser.parse_args()
    print(f's: {args.source}; f: {args.format}; r: {args.result_file}')

    res_format = args.format
    source_file = args.source

    if not source_file or '.' not in source_file:
        raise TypeError(f"Incorrect source path : {source_file}")

    source_format = source_file[source_file.find('.') + 1:]
    if source_format == res_format:
        return "Same with source format."

    serializer_source = get_serializer(source_format)
    serializer_result = get_serializer(res_format)

    loaded = serializer_source.load(source_file)
    if args.result_file:
        serializer_result.dump(loaded, args.result_file)
    else:
        return serializer_result.dumps(loaded)


def main():
    serialized = serializer()
    if serialized:
        print(serialized)
    print("Success.")


if __name__ == "__main__":
    main()
