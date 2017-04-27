package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("personList")
public class PersonList extends EntityQuery<Person> {

	private static final String EJBQL = "select person from Person person";

	private static final String[] RESTRICTIONS = {
			"lower(person.id) like lower(concat(#{personList.person.id},'%'))",
			"lower(person.first) like lower(concat(#{personList.person.first},'%'))",
			"lower(person.initials) like lower(concat(#{personList.person.initials},'%'))",
			"lower(person.last) like lower(concat(#{personList.person.last},'%'))",
			"lower(person.middle) like lower(concat(#{personList.person.middle},'%'))",
			"lower(person.nick) like lower(concat(#{personList.person.nick},'%'))",
			"lower(person.other) like lower(concat(#{personList.person.other},'%'))",};

	private Person person = new Person();

	public PersonList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public Person getPerson() {
		return person;
	}
}
