import ArrayList

public class Example {
  private ArrayList<String> names;

  public Example() {
    names = new ArrayList<>();
  }

  public void addName(String name) {
    names.add(name);
  }

  public List<String> getNames() {
    return new ArrayList<>(names);
  }
}
