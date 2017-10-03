package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("personlifeHome")
public class PersonlifeHome extends EntityHome<Personlife> {

	@In(create = true)
	PersonHome personHome;

	public void setPersonlifeId(String id) {
		setId(id);
	}

	public String getPersonlifeId() {
		return (String) getId();
	}

	@Override
	protected Personlife createInstance() {
		Personlife personlife = new Personlife();
		return personlife;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		Person person = personHome.getDefinedInstance();
		if (person != null) {
			getInstance().setPerson(person);
		}
	}

	public boolean isWired() {
		return true;
	}

	public Personlife getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
